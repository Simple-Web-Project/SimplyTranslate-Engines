import lxml.html as lxml
from urllib.parse import urlencode, quote
import json
import re

if __name__ != "__main__":
    from .utils import async_get, async_post
else:
    import asyncio
    from utils import async_get, async_post


class GoogleTranslateEngine:
    name = "google"
    display_name = "Google"

    def get_supported_source_languages(self):
        return {"Autodetect": "auto", **self.get_supported_target_languages()}

    def get_supported_target_languages(self):
        return {
            "Afrikaans": "af",
            "Albanian": "sq",
            "Amharic": "am",
            "Arabic": "ar",
            "Armenian": "hy",
            "Azerbaijani": "az",
            "Basque": "eu",
            "Belarusian": "be",
            "Bengali": "bn",
            "Bosnian": "bs",
            "Bulgarian": "bg",
            "Catalan": "ca",
            "Cebuano": "ceb",
            "Chichewa": "ny",
            "Chinese": "zh-CN",
            "Corsican": "co",
            "Croatian": "hr",
            "Czech": "cs",
            "Danish": "da",
            "Dutch": "nl",
            "English": "en",
            "Esperanto": "eo",
            "Estonian": "et",
            "Filipino": "tl",
            "Finnish": "fi",
            "French": "fr",
            "Frisian": "fy",
            "Galician": "gl",
            "Georgian": "ka",
            "German": "de",
            "Greek": "el",
            "Gujarati": "gu",
            "Haitian Creole": "ht",
            "Hausa": "ha",
            "Hawaiian": "haw",
            "Hebrew": "iw",
            "Hindi": "hi",
            "Hmong": "hmn",
            "Hungarian": "hu",
            "Icelandic": "is",
            "Igbo": "ig",
            "Indonesian": "id",
            "Irish": "ga",
            "Italian": "it",
            "Japanese": "ja",
            "Javanese": "jw",
            "Kannada": "kn",
            "Kazakh": "kk",
            "Khmer": "km",
            "Kinyarwanda": "rw",
            "Korean": "ko",
            "Kurdish (Kurmanji)": "ku",
            "Kyrgyz": "ky",
            "Lao": "lo",
            "Latin": "la",
            "Latvian": "lv",
            "Lithuanian": "lt",
            "Luxembourgish": "lb",
            "Macedonian": "mk",
            "Malagasy": "mg",
            "Malay": "ms",
            "Malayalam": "ml",
            "Maltese": "mt",
            "Maori": "mi",
            "Marathi": "mr",
            "Mongolian": "mn",
            "Myanmar (Burmese)": "my",
            "Nepali": "ne",
            "Norwegian": "no",
            "Odia (Oriya)": "or",
            "Pashto": "ps",
            "Persian": "fa",
            "Polish": "pl",
            "Portuguese": "pt",
            "Punjabi": "pa",
            "Romanian": "ro",
            "Russian": "ru",
            "Samoan": "sm",
            "Scots Gaelic": "gd",
            "Serbian": "sr",
            "Sesotho": "st",
            "Shona": "sn",
            "Sindhi": "sd",
            "Sinhala": "si",
            "Slovak": "sk",
            "Slovenian": "sl",
            "Somali": "so",
            "Spanish": "es",
            "Sundanese": "su",
            "Swahili": "sw",
            "Swedish": "sv",
            "Tajik": "tg",
            "Tamil": "ta",
            "Tatar": "tt",
            "Telugu": "te",
            "Thai": "th",
            "Turkish": "tr",
            "Turkmen": "tk",
            "Ukrainian": "uk",
            "Urdu": "ur",
            "Uyghur": "ug",
            "Uzbek": "uz",
            "Vietnamese": "vi",
            "Welsh": "cy",
            "Xhosa": "xh",
            "Yiddish": "yi",
            "Yoruba": "yo",
            "Zulu": "zu",
        }

    def detect_language(self, text):
        return None

    def get_tts(self, text, language):
        if text == None or language == None:
            return None
        elif len(text) == 0 or len(language) == 0:
            return None

        if language == "auto":
            language = "en"

        params = urlencode({"tl": language, "q": text.strip(), "client": "tw-ob"})
        return f"https://translate.google.com/translate_tts?{params}"

    async def translate(self, text, to_language, from_language="auto"):
        my_map = {}
        try:
            url = "https://translate.google.com/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&rt=c"

            req = json.dumps([[text, from_language, to_language, True], [None]])
            req = [[["MkEWBc", req, None, "generic"]]]
            req = "f.req=" + quote(json.dumps(req))  # URL encode this

            print(f"Getting the response for {text}")
            response_text = await async_post(
                url,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=req,
            )

            num_match = re.search(r"\n(\d+)\n", response_text)
            front_pad = num_match.span()[1]
            end_num = front_pad + int(num_match.groups()[0]) - 1

            data = json.loads(response_text[front_pad:end_num])
            data = data[0][2]
            data = json.loads(data)

            try:
                my_map["definitions"] = {}
                for x in range(0, len(data[3][1][0])):
                    definition_type = data[3][1][0][x][0]
                    my_map["definitions"][definition_type] = []
                    for i in range(0, len(data[3][1][0][x][1])):
                        my_map["definitions"][definition_type].append({})
                        definition_box = data[3][1][0][x][1][i]

                        try:
                            my_map["definitions"][definition_type][i][
                                "dictionary"
                            ] = definition_box[4][0][0]
                        except:
                            pass

                        try:
                            my_map["definitions"][definition_type][i][
                                "definition"
                            ] = definition_box[0]
                        except:
                            pass

                        try:
                            use_in_sentence = definition_box[1]
                            if use_in_sentence is not None:
                                my_map["definitions"][definition_type][i][
                                    "use-in-sentence"
                                ] = use_in_sentence
                        except:
                            pass

                        try:
                            synonyms = definition_box[5]
                            my_map["definitions"][definition_type][i]["synonyms"] = {}
                            for synonym_box in synonyms:
                                synonym_type = ""
                                try:
                                    synonym_type = synonym_box[1][0][0]
                                except:
                                    pass
                                my_map["definitions"][definition_type][i]["synonyms"][
                                    synonym_type
                                ] = []

                                try:
                                    synonym_list = synonym_box[0]
                                    for synonym_type_word in synonym_list:
                                        try:
                                            my_map["definitions"][definition_type][i][
                                                "synonyms"
                                            ][synonym_type].append(synonym_type_word[0])
                                        except:
                                            pass
                                except:
                                    pass

                        except:
                            pass
            except:
                pass

            try:
                translation_box = data[3][5][0]
                my_map["translations"] = {}
                for x in range(0, len(translation_box)):
                    try:
                        translation_type = translation_box[x][0]
                        my_map["translations"][translation_type] = {}
                        translation_names_box = translation_box[x][1]
                        for i in range(0, len(translation_names_box)):
                            my_map["translations"][translation_type][
                                translation_names_box[i][0]
                            ] = {}
                            frequency = str(translation_names_box[i][3])
                            if frequency == "3":
                                frequency = "1"
                            elif frequency == "1":
                                frequency = "3"

                            my_map["translations"][translation_type][
                                translation_names_box[i][0]
                            ]["words"] = []
                            for z in range(0, len(translation_names_box[i][2])):
                                my_map["translations"][translation_type][
                                    translation_names_box[i][0]
                                ]["words"].append(translation_names_box[i][2][z])

                            my_map["translations"][translation_type][
                                translation_names_box[i][0]
                            ]["frequency"] = (frequency + "/3")
                    except:
                        pass

            except:
                pass
        except:
            pass

        response_text = await async_get(
            "https://translate.google.com/m",
            params={"tl": to_language, "hl": to_language, "q": text},
        )

        doc = lxml.fromstring(response_text)
        for container in doc.find_class("result-container"):
            my_map["translated-text"] = container.text_content()

        return my_map


async def test():
    print(
        await asyncio.gather(
            GoogleTranslateEngine().translate("Hallo", "en", "de"),
            GoogleTranslateEngine().translate("Bonjour", "en", "fr"),
            GoogleTranslateEngine().translate("Hola", "en", "es"),
        )
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
