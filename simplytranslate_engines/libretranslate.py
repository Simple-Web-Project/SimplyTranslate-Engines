import json
import requests


class LibreTranslateEngine:
    def __init__(self, url, api_key=None):
        self.url = url
        self.api_key = api_key

    name = "libre"
    display_name = "LibreTranslate"

    _supported_languages = None

    def get_supported_source_languages(self):
        return {"Autodetect": "auto", **self.get_supported_target_languages()}

    def get_supported_target_languages(self):
        if self._supported_languages is not None:
            return self._supported_languages

        request = requests.post(f"{self.url}/languages")
        response = json.loads(request.text)

        self._supported_languages = {lang["name"]: lang["code"] for lang in response}

        return self._supported_languages

    def detect_language(self, text):
        form = {"q": text}

        if self.api_key is not None:
            form["api_key"] = self.api_key

        r = requests.post(f"{self.url}/detect", json=form)

        response = json.loads(r.text)

        if type(response) != list:
            return (
                response["error"]
                if "error" in response
                else "odd, something went wrong"
            )

        return max(response, key=lambda item: item["confidence"])["language"]

    def get_tts(self, text, language):
        return None

    def translate(self, text, to_language, from_language="auto"):
        myMap = {}
        form = {"q": text, "source": from_language, "target": to_language}

        if self.api_key is not None:
            form["api_key"] = self.api_key

        r = requests.post(f"{self.url}/translate", json=form)

        response = json.loads(r.text)
        if "translatedText" in response:
            translated_text = response["translatedText"]
        elif "error" in response:
            translated_text = response["error"]
        else:
            translated_text = "odd, something went wrong"
        return {"translated-text": translated_text}


if __name__ == "__main__":
    print(
        LibreTranslateEngine("https://libretranslate.de").translate(
            "dies ist ein sehr einfacher und politisch korrekter test", "en"
        )
    )
