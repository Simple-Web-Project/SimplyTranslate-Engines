import json
import requests

supported_languages = {
    "English": "en",
    "Arabic": "ar",
    "Chinese": "zh",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Spanish": "es",
}

def translate(text, to_language, from_language="auto", libretranslate_url="https://libretranslate.com/translate"):
    r = requests.post(
        libretranslate_url,
        json={
            "q": text,
            "source": from_language,
            "target": to_language
        })

    #response = dict(r.text)
    response = json.loads(r.text)
    if "translatedText" in response:
        return response["translatedText"]
    elif "error" in response:
        return response["error"]
    else:
        return "odd, something went wrong"


if __name__ == "__main__":
    print(translate("lutsch meinen schwanz", "en"))
