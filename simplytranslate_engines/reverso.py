import requests


class ReversoTranslateEngine:
    name = "reverso"
    display_name = "Reverso"

    def get_supported_source_languages(self):
        return {"Autodetect": "auto", **self.get_supported_target_languages()}

    def get_supported_target_languages(self):
        return {
            "Arabic": "ara",
            "Chinese (Simplified)": "chi",  # marketed as just "Chinese"
            "Dutch": "dut",
            "English": "eng",
            "French": "fra",
            "German": "ger",
            "Hebrew": "heb",
            "Italian": "ita",
            "Japanese": "jpn",
            "Korean": "kor",
            "Polish": "pol",
            "Portuguese": "por",
            "Romanian": "rum",
            "Russian": "rus",
            "Spanish": "spa",
            "Swedish": "swe",
            "Turkish": "tur",
            "Ukrainian": "ukr",
        }

    def call_api(self, text, to_language, from_language):
        # `contextResults` must be False for language detection
        r = requests.post(
            "https://api.reverso.net/translate/v1/translation",
            json={
                "format": "text",
                "from": from_language,
                "to": to_language,
                "input": text,
                "options": {
                    "sentenceSplitter": False,
                    "origin": "translation.web",
                    "contextResults": False,
                    "languageDetection": True,
                },
            },
            headers={
                "Content-Type": "application/json",
                "User-Agent": "",  # Either empty or a browser User-Agent
            },
        ).json()
        return r

    def detect_language(self, text):
        # Any language pair works here, does not affect result
        r = self.call_api(text, "eng", "fra")
        return r["languageDetection"]["detectedLanguage"]

    def get_tts(self, text, language):
        return None

    def translate(self, text, to_language, from_language="auto"):
        if from_language == "auto":
            from_language = self.detect_language(text)
        if from_language == to_language:
            return text
        r = self.call_api(text, to_language, from_language)
        return r["translation"][0]


if __name__ == "__main__":
    print(
        ReversoTranslateEngine().translate(
            "there is an impostor among us", "ger", "eng"
        )
    )
