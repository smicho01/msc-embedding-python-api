import requests
import os
from transformers import pipeline

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


## Check if text is valid English
# Load the language identification pipeline
lang_identifier = pipeline('text-classification', model='papluca/xlm-roberta-base-language-detection')

# Load the spam detection pipeline
spam_detector = pipeline('text-classification', model='unitary/toxic-bert')


def is_english(text):
    result = lang_identifier(text)
    return result[0]['label'] == 'en'


def is_not_spam(text):
    result = spam_detector(text)
    return result[0]['label'] != 'spam'


def check_text(text):
    if is_english(text):
        if is_not_spam(text):
            return True
        else:
            return False
    else:
        return False
