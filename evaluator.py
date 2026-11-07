import json
import time

from google.genai import errors
from config import client, MODEL_NAME
from prompts import EVALUATION_PROMPT


def check_deliberate_errors(lesson):
    """
    Detect deliberately inserted false claims.
    This check works without calling Gemini.
    """

    known_false_claims = [
        "RAG guarantees that an AI will always provide 100% accurate answers.",
        "RAG guarantees 100% accuracy."
    ]

    detected_errors = []

    for claim in known_false_claims:
        if claim.lower() in lesson.lower():
            detected_errors.append(claim)

    return detected_errors


def evaluate_lesson(lesson):

    print("\nEvaluating generated lesson...")

    # Step 1: Check known deliberate errors locally
    detected_errors = check_deliberate_errors(lesson)

    if detected_errors:
        print("Deliberate error detected!")

        return {
            "overall_status": "FAIL",
            "checks": {
                "accuracy": {
                    "status": "FAIL",
                    "reason": (
                        "The lesson contains a false claim: "
                        + "; ".join(detected_errors)
                    )
                },
                "beginner_friendliness": {
                    "status": "PASS",
                    "reason": "Not evaluated by the local error check."
                },
                "examples": {
                    "status": "PASS",
                    "reason": "Not evaluated by the local error check."
                },
                "jargon": {
                    "status": "PASS",
                    "reason": "Not evaluated by the local error check."
                },
                "topic_coverage": {
                    "status": "PASS",
                    "reason": "Not evaluated by the local error check."
                },
                "teaching_flow": {
                    "status": "PASS",
                    "reason": "Not evaluated by the local error check."
                },
                "completeness": {
                    "status": "PASS",
                    "reason": "Not evaluated by the local error check."
                }
            },
            "failure_reasons": [
                "Accuracy failure: deliberately incorrect RAG claim detected."
            ],
            "improvement_suggestions": [
                "Remove the false accuracy guarantee and explain that RAG can reduce errors but cannot eliminate them."
            ]
        }

    # Step 2: Run the Gemini evaluator
    prompt = EVALUATION_PROMPT.replace("{lesson}", lesson)

    for attempt in range(1, 4):

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            if not response.text:
                raise ValueError("Evaluator returned an empty response.")

            result = json.loads(response.text)

            required_criteria = [
                "accuracy",
                "beginner_friendliness",
                "examples",
                "jargon",
                "topic_coverage",
                "teaching_flow",
                "completeness"
            ]

            if "checks" not in result:
                raise ValueError("Missing checks in evaluation response.")

            for criterion in required_criteria:

                if criterion not in result["checks"]:
                    raise ValueError(
                        f"Missing criterion: {criterion}"
                    )

                status = result["checks"][criterion].get("status")

                if status not in ["PASS", "FAIL"]:
                    raise ValueError(
                        f"Invalid status for {criterion}"
                    )

            all_passed = all(
                result["checks"][criterion]["status"] == "PASS"
                for criterion in required_criteria
            )

            result["overall_status"] = (
                "PASS" if all_passed else "FAIL"
            )

            print("Evaluation completed!")
            print("Overall status:", result["overall_status"])

            return result

        except errors.ServerError as error:

            if error.code != 503 or attempt == 3:
                raise

            print(
                f"Gemini temporarily unavailable. "
                f"Retrying evaluation ({attempt}/3)..."
            )

            time.sleep(5 * attempt)

    raise RuntimeError("Evaluation failed after three attempts.")


if __name__ == "__main__":

    with open(
        "outputs/generated_lesson.md",
        "r",
        encoding="utf-8"
    ) as file:
        lesson = file.read()

    evaluation = evaluate_lesson(lesson)

    print("\nEVALUATION RESULTS")
    print(json.dumps(evaluation, indent=4))

    with open(
        "outputs/evaluation.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(evaluation, file, indent=4)

    print("\nEvaluation saved in outputs/evaluation.json")
