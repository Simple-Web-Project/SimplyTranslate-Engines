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

    def get_supported_source_languages(self):
        return {"Autodetect": "auto", **self.get_supported_target_languages()}

    def get_supported_target_languages(self): return {
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
            "Swedish": "SV"
        }

    def detect_language(self, text):
        return None

    def get_tts(self, text, language):
        return None

    def translate(self, text, to_language, from_language="auto"):
        myMap = {}

        # NOTE: this takes insanely long to process
        translation = self.deepl.translate(text, to_language, from_language)
        myMap['translated-text'] = translation
        return myMap

if __name__ == "__main__":
    engine = DeeplEngine()

    for i in range(1, 15):
        print(engine.translate("You are on the testing lane", "EN", "DE"))
        time.sleep(i)

