from config import client, MODEL_NAME
from prompts import LESSON_GENERATION_PROMPT


def generate_lesson(topic, feedback=None):
    """
    Generate a beginner-friendly lesson using Gemini.

    Args:
        topic: The topic to teach.
        feedback: Evaluator feedback from a previous failed attempt.

    Returns:
        Generated lesson as text.
    """

    prompt = LESSON_GENERATION_PROMPT.format(topic=topic)

    # Include evaluator feedback during regeneration
    if feedback:
        prompt += f"""

IMPORTANT: Your previous lesson failed evaluation.

EVALUATOR FEEDBACK:
{feedback}

Improve the lesson by addressing every failure.
Do not repeat the previous mistakes.
Generate the complete corrected lesson.
"""

    print(f"\nGenerating lesson for: {topic}")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        lesson = response.text.strip()

        print("Lesson generated successfully!")

        return lesson

    except Exception as error:
        print(f"Lesson generation failed: {error}")
        raise


# Test the lesson generator independently
if __name__ == "__main__":

    topic = "Introduction to RAG"

    lesson = generate_lesson(topic)

    print("\n" + "=" * 60)
    print("GENERATED BEGINNER LESSON")
    print("=" * 60)

    print(lesson)

    # Save the generated lesson
    with open(
        "outputs/generated_lesson.md",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(lesson)

    print("\nLesson saved in outputs/generated_lesson.md")
