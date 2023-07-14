import requests

# Source: https://huggingface.co/AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru?context=My+name+is+Wolfgang+and+I+live+in+Berlin&question=Hello

API_URL = "https://api-inference.huggingface.co/models/AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru"
headers = {"Authorization": "Bearer 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"}


async def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

