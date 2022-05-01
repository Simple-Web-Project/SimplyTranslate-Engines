# e code included in this file was originally inspired by https://github.com/KeKsBoTer/deepl-cli/blob/master/deepl.py
# Sadly I could find no license file attached to this

import requests
import time
import json
from datetime import datetime
from translatepy.translators.deepl import DeeplTranslate



class DeeplEngine:
    name = "deepl"
    display_name = "DeepL (Testing)"

    def __init__(self):
        self.session = requests.Session()
        self.delay_begin = None
        self.deepl = DeeplTranslate()

    async def get_supported_source_languages(self):
        return {"Autodetect": "auto", **await self.get_supported_target_languages()}

    async def get_supported_target_languages(self):
        return {
            "Bulgarian": "BG",
            "Chinese": "ZH",
            "Czech": "CS",
            "Danish": "DA",
            "Dutch": "NL",
            "English": "EN",
            "Estonian": "ET",
            "Finnish": "FI",
            "French": "FR",
            "German": "DE",
            "Greek": "EL",
            "Hungarian": "HU",
            "Italion": "IT",
            "Japanese": "JA",
            "Latvian": "LV",
            "Lithuanian": "LT",
            "Polish": "PL",
            "Portugese": "PT",
            "Romanian": "RO",
            "Russian": "RU",
            "Slovak": "SK",
            "Slovenian": "SL",
            "Spanish": "ES",
            "Swedish": "SV",
        }

    async def detect_language(self, text: str):
        return None

    async def get_tts(self, text: str, language: str):
        return None

    async def translate(self, text: str, to_language: str, from_language: str="auto"):
        # NOTE: this takes insanely long to process
        try:
            translation = self.deepl.translate(text, to_language, from_language)
        except Exception as e:
            translation = "Failed to translate! Sorry!"

        return {
            "translated-text": translation,
            "source_language": from_language
        }

async def test():
    e = DeeplEngine()
    print(
        await asyncio.gather(
            e.translate("Hallo", "en", "de"),
            e.translate("Bonjour", "en", "fr"),
            e.translate("Hola", "en", "de"),
        )
    )


if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
