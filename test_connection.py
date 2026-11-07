print("STEP 1: Starting test")

from config import client, MODEL_NAME

print("STEP 2: Gemini client imported")
print("STEP 3: Model:", MODEL_NAME)

try:
    print("STEP 4: Sending request to Gemini...")

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents="Explain RAG in one sentence."
    )

    print("STEP 5: Response received!")
    print(response.text)

except Exception as e:
    print("GEMINI ERROR:", repr(e))
