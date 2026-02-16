import requests
import json
import time
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

test_models = [
    "meta-llama/llama-3.3-70b-instruct:free",      
    "deepseek/deepseek-r1-0528:free",             
    "google/gemma-3-27b-it:free",                 
    "qwen/qwen3-coder:free",                         
    "liquid/lfm-2.5-1.2b-thinking:free",            
]

def test_models_all(models: list):
    for model in models:
        print(f"Testing {model}...")
        start = time.time()
        response = or_request(model)
        duration = time.time() - start
        status = response.status_code

        if status == 200:
            data = response.json()
            prompt_tokens = data["usage"]["prompt_tokens"]
            completion_tokens = data["usage"]["completion_tokens"]
            total_tokens = data["usage"]["total_tokens"]
            cost = data["usage"]["cost"]
            print("  Connectivity: PASS")
            print(f"  Response latency: {duration:.2f}s")
            print(f"  Prompt tokens: {prompt_tokens}")
            print(f"  Completion tokens: {completion_tokens}")
            print(f"  Total tokens: {total_tokens}")
            print(f"  Response Cost: {cost}")
        else:
            print(f"  FAIL ({status})")

        time.sleep(10)


def test_error_handling():
    print("Testing bad API key...")
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": "Bearer fake-key-12345"},
        json={
            "model": "meta-llama/llama-3.3-70b-instruct:free",
            "messages": [{"role": "user", "content": "hello"}],
        },
        timeout=30,
    )
    print(f"  Bad API key: {response.status_code}")
    time.sleep(10)

    print("Testing invalid model...")
    response = or_request("not-a-real/model-name")
    print(f"  Invalid model: {response.status_code}")
    time.sleep(10)

    print("Testing empty messages...")
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "meta-llama/llama-3.3-70b-instruct:free",
            "messages": [],
        },
        timeout=30,
    )
    print(f"  Empty messages: {response.status_code}")


def or_request(model: list, prompt: str ="Hello, how are you?"): 
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}"
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=30
    )

    return response


test_models_all(test_models)
test_error_handling()