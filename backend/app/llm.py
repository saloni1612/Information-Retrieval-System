import requests

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "llama3"  # change to your model like 'mistral' or 'llama3'

def query_llm(prompt: str) -> str:
    """Send a prompt to the local LLM and return the response."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.RequestException as e:
        print(f"[LLM Error] {e}")
        return "[LLM Error] Unable to generate a response."
