import requests
import os

# Environment variable for Hugging Face token
hf_token = os.getenv('HF_TOKEN', '')
if not hf_token:
    raise ValueError("No HF_TOKEN found in environment variables")

embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


def generate_embedding(text):
    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text}
    )
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")
    return response.json()
