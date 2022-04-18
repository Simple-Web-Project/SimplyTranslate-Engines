import requests

#TODO: Make this actually async!

class ReversoTranslateEngine:
    name = "reverso"
    display_name = "Reverso"

    async def get_supported_source_languages(self):
        return {"Autodetect": "auto", **self.get_supported_target_languages()}

    async def get_supported_target_languages(self):
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

    async def call_api(self, text, to_language, from_language) -> dict:
        # `contextResults` must be False for language detection
        r = requests.post(
            "https://api.reverso.net/translate/v1/translation",
            json={
                "format": "text",
                "from": from_language,
                "to": to_language,
                "input": text,
                "options": {
                    "sentenceSplitter": "false",
                    "origin": "translation.web",
                    "contextResults": "false",
                    "languageDetection": "true",
                },
            },
            headers={
                "Content-Type": "application/json",
                "User-Agent": "",  # Either empty or a browser User-Agent
            },
        ).json()
        return r

    async def detect_language(self, text):
        # Any language pair works here, does not affect result
        r = await self.call_api(text, "eng", "fra")
        return r["languageDetection"]["detectedLanguage"]

    async def get_tts(self, text, language):
        return None

    async def translate(self, text, to_language, from_language="auto"):
        if from_language == "auto":
            from_language = self.detect_language(text)
        if from_language == to_language:
            translated_text = text
        else:
            r = await self.call_api(text, to_language, from_language)
            print(r)
            translated_text = r["translation"][0]
        return {"translated-text": translated_text}


async def test():
    e = ReversoTranslateEngine()
    print(
        await asyncio.gather(
            e.translate("Hallo", "en", "de"),
            e.translate("Bonjour", "en", "fr"),
            e.translate("Hola", "en", "es"),
        )
    )

    print(await e.detect_language("Rechtsanwalt"))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
