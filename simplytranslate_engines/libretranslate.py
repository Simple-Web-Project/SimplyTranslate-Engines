import json
import requests

class LibreTranslateEngine:
    def __init__(self, url="https://libretranslate.com"):
        self.url = url

    name = "libre"

    def get_supported_languages(self):
        return {
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

    def translate(self, text, to_language, from_language="auto"):
        r = requests.post(
            f"{self.url}/translate",
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
    print(LibreTranslateEngine().translate("lutsch meinen schwanz", "en"))
