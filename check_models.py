from config import client

print("Checking available Gemini models...\n")

try:
    for model in client.models.list():
        actions = getattr(model, "supported_actions", []) or []

        if "generateContent" in actions:
            print("Model:", model.name)
            print("Supported actions:", actions)
            print("-" * 40)

except Exception as e:
    print("ERROR:", repr(e))
