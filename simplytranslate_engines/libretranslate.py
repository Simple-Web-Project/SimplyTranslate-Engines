import json
import requests

class LibreTranslateEngine:
    def __init__(self, url, api_key=None):
        self.url = url
        self.api_key = api_key

    name = "libre"

    _supported_languages = None

    def get_supported_languages(self):
        if self._supported_languages is not None:
            return self._supported_languages

        request = requests.post(f"{self.url}/languages")
        response = json.loads(request.text)

        self._supported_languages = {
            lang["name"]: lang["code"] for lang in response
        }

        return self._supported_languages

    def translate(self, text, to_language, from_language="auto"):
        form = {
            "q": text,
            "source": from_language,
            "target": to_language
        }

        if self.api_key is not None:
            form["api_key"] = self.api_key

        r = requests.post(f"{self.url}/translate", json=form)

        response = json.loads(r.text)
        if "translatedText" in response:
            return response["translatedText"]
        elif "error" in response:
            return response["error"]
        else:
            return "odd, something went wrong"

if __name__ == "__main__":
    print(LibreTranslateEngine("https://libretranslate.de").translate("lutsch meinen schwanz", "en"))
