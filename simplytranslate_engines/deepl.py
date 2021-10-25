# The code included in this file was originally inspired by https://github.com/KeKsBoTer/deepl-cli/blob/master/deepl.py
# Sadly I could find no license file attached to this

import requests
import time
import json

class DeeplEngine:
    name = "deepl"

    def __init__(self):
        self.session = requests.Session()

    def get_supported_languages(self):
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
                #WIP: According to my testing it takes 8 seconds so a "Too many requests" is no longer true
                # but for now we just request a new Session, which might just fix the issue but I doubt it
                self.session = requests.Session()
                return "error: Too many requests at this time, please wait a few seconds"

            return f"error: {error_message}"

        # There are potentially more translations attached to this request, but we ignore them for now
        translation = j_content["result"]["translations"][0]["beams"][0]["postprocessed_sentence"]

        return translation

if __name__ == "__main__":
    engine = DeeplEngine()

    for i in range(8, 15):
        print(engine.translate("You can't fuck with me", "EN", "DE"))
        time.sleep(i)

