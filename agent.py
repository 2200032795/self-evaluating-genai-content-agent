import json

from generator import generate_lesson
from evaluator import evaluate_lesson
from memory import (
    initialize_memory,
    save_run,
    get_previous_feedback
)


MAX_ATTEMPTS = 3


def run_content_agent(topic, demo_mode=False):

    initialize_memory()

    print("\n" + "=" * 60)
    print("SELF-EVALUATING CONTENT GENERATION AGENT")
    print("=" * 60)

    feedback = get_previous_feedback(topic)

    if feedback:
        print("\nPrevious learning retrieved from memory!")
    else:
        print("\nNo previous failure memory found.")

    rejection_log = []
    final_lesson = None
    final_evaluation = None

    for attempt in range(1, MAX_ATTEMPTS + 1):

        print(f"\nATTEMPT {attempt} OF {MAX_ATTEMPTS}")

        try:
            lesson = generate_lesson(topic, feedback)

        except Exception as error:
            print("\nGeneration service unavailable:", error)
            return None

        # Inject a known error only for the demonstration's first attempt.
        if demo_mode and attempt == 1:
            lesson += (
                "\n\nRAG guarantees that an AI will always "
                "provide 100% accurate answers.\n"
            )
            print("\nDEMO: Deliberately incorrect claim inserted.")

        try:
            evaluation = evaluate_lesson(lesson)

        except Exception as error:
            print("\nEvaluation service unavailable:", error)
            return {
                "lesson": lesson,
                "evaluation": None,
                "rejection_log": rejection_log,
                "status": "EVALUATION_INTERRUPTED"
            }

        if evaluation["overall_status"] == "PASS":

            print("\nLesson passed all evaluation criteria!")

            final_lesson = lesson
            final_evaluation = evaluation
            break

        print("\nLesson rejected. Preparing regeneration...")

        rejection_log.append({
            "attempt": attempt,
            "status": "FAIL",
            "failure_reasons": evaluation.get(
                "failure_reasons", []
            ),
            "checks": evaluation["checks"]
        })

        feedback = json.dumps(evaluation, indent=4)

        final_lesson = lesson
        final_evaluation = evaluation

    if final_evaluation["overall_status"] == "PASS":

        with open(
            "outputs/final_lesson.md",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(final_lesson)

        print("\nFinal approved lesson saved!")

    else:
        print("\nMaximum attempts reached. No lesson approved.")

    with open(
        "outputs/rejection_log.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(rejection_log, file, indent=4)

    save_run(
        topic,
        final_evaluation["overall_status"],
        attempt,
        rejection_log
    )

    print("\n" + "=" * 60)
    print("AGENT EXECUTION SUMMARY")
    print("=" * 60)

    print("Total attempts:", attempt)
    print("Final status:", final_evaluation["overall_status"])
    print("Rejected attempts:", len(rejection_log))

    return {
        "lesson": final_lesson,
        "evaluation": final_evaluation,
        "rejection_log": rejection_log,
        "status": final_evaluation["overall_status"]
    }


if __name__ == "__main__":

    run_content_agent(
        "Introduction to RAG",
        demo_mode=True
    )
