from transformers import pipeline
from helpers import get_settings

settings = get_settings()
translator = pipeline("translation", model=settings.TRANSLATION_MODEL)

def translate_arabic_to_english(prompt: str) -> str:
    return translator(prompt)[0]['translation_text']