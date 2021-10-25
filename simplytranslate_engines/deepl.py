# The code included in this file was originally inspired by https://github.com/KeKsBoTer/deepl-cli/blob/master/deepl.py
# Sadly I could find no license file attached to this

import requests
import time
import json

class DeeplEngine:
    name = "deepl"

    def get_supported_languages(self):
        return {
            "German": "DE",
            "English": "EN",
            "French": "FR"
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
        response = requests.post("https://www2.deepl.com/jsonrpc", params={}, json=data)

        j_content = json.loads(response.content)

        if "error" in j_content:
            return "error: "  + j_content["error"]["message"]

        # There are potentially more translations attached to this request, but we ignore them for now
        translation = j_content["result"]["translations"][0]["beams"][0]["postprocessed_sentence"]

        return translation

if __name__ == "__main__":
    print(DeeplEngine().translate("You can't fuck with me", "EN", "DE"))
