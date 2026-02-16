import requests

API_KEY = "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"

models_response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": f"Bearer {API_KEY}"},
    timeout=30
)

all_models = models_response.json()["data"]
free_models = [m["id"] for m in all_models if ":free" in m["id"]]

for m in free_models:
    print(m)