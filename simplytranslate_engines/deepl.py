# The code included in this file was originally inspired by https://github.com/KeKsBoTer/deepl-cli/blob/master/deepl.py
# Sadly I could find no license file attached to this

import requests
import time
import json
from datetime import datetime

class DeeplEngine:
    name = "deepl"
    display_name = "DeepL (Testing)"

    def __init__(self):
        self.session = requests.Session()
        self.delay_begin = None

    def get_supported_source_languages(self):
        langs = {"Autodetect": "auto"}
        langs = langs | self.get_supported_target_languages()
        return langs

    def get_supported_target_languages(self):
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
            "Swedish": "SV"
        }

    def detect_language(self, text):
        return None

    def get_tts(self, text, language):
        return None

    def translate(self, text, to_language, from_language="auto"):
        if self.delay_begin != None:
            difference = datetime.now() - self.delay_begin
            if difference.seconds > 120:
                self.delay_begin = None
                self.session = requests.Session()
            else:
                return "error: Too many requests, please wait a few seconds"

        data = {
            "jsonrpc": "2.0",
            "method": "LMT_handle_jobs",
            "params": {
                "jobs": [
                    {
                        "kind": "default",
                        "raw_en_sentence": text,
                        "raw_en_context_before": [],
                        "raw_en_context_after": [],
                        "quality": "fast"
                    }
                ],
                "lang": {
                    "user_preferred_langs": [from_language, to_language],
                    "source_lang_user_selected": from_language,
                    "target_lang": to_language
                },
                "priority": -1,
                "timestamp": int(time.time()*1000)
            }
        }
        response = self.session.post("https://www2.deepl.com/jsonrpc", params={}, json=data)

        j_content = json.loads(response.content)

        if "error" in j_content:
            error_message = j_content["error"]["message"]
            if error_message == "Too many requests":
                # Introduce an artificial delay until the next request can be made
                # So the server doesn't end up banning our IP
                self.delay_begin = datetime.now()
                return "error: Too many requests, please wait a few seconds"

            return f"error: {error_message}"

        # There are potentially more translations attached to this request, but we ignore them for now
        translation = j_content["result"]["translations"][0]["beams"][0]["postprocessed_sentence"]

        return translation

if __name__ == "__main__":
    engine = DeeplEngine()

    for i in range(1, 15):
        print(engine.translate("You can't fuck with me", "EN", "DE"))
        time.sleep(i)

