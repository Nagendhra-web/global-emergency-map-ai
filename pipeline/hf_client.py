import os, requests

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API = "https://api-inference.huggingface.co/models"
TRANSLATION_MODEL = os.getenv("HF_TRANSLATION_MODEL", "facebook/nllb-200-distilled-600M")

def _hf_post(model, payload):
    if not HF_TOKEN:
        return None, "no_token"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    url = f"{HF_API}/{model}"
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    if r.status_code == 503:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
    if not r.ok:
        return None, f"err_{r.status_code}"
    return r.json(), None

def translate_if_needed(text, lang_hint):
    if not text:
        return text
    if not HF_TOKEN:
        return text
    if (lang_hint or "en").lower().startswith("en"):
        return text
    payload = {"inputs": text, "parameters": {"target_language": "eng"}}
    data, err = _hf_post(TRANSLATION_MODEL, payload)
    if err or not data:
        return text
    if isinstance(data, list) and data and isinstance(data[0], dict) and "translation_text" in data[0]:
        return data[0]["translation_text"]
    if isinstance(data, dict) and "translation_text" in data:
        return data["translation_text"]
    return text
