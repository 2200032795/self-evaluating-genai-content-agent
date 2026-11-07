from evaluator import evaluate_lesson

incorrect_lesson = """
# Introduction to RAG

RAG guarantees that an AI will always provide 100% accurate answers.
"""

result = evaluate_lesson(incorrect_lesson)

print("\nTEST RESULT:", result["overall_status"])
print("ACCURACY:", result["checks"]["accuracy"]["status"])
print("REASON:", result["checks"]["accuracy"]["reason"])

assert result["overall_status"] == "FAIL"
assert result["checks"]["accuracy"]["status"] == "FAIL"

print("\nSUCCESS: The evaluator caught the deliberate error!")
