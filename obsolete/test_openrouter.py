import requests

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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"
    },
    json={
        "model": "openrouter/free",
        "messages": [{"role": "user", "content": "Hello, how are you?"}],
    }
)

print(response.status_code)
print(response.json())