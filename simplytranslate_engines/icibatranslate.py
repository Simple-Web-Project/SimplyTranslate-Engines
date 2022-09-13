import requests
import hashlib
import asyncio

#TODO: Make this truly async!
class IcibaTranslateEngine:
    name = "iciba"
    display_name = "ICIBA"

    async def get_supported_source_languages(self):
        return {"Autodetect": "auto", **await self.get_supported_target_languages()}

    async def get_supported_target_languages(self):
        return {
            # ICIBA does have an API, but they return Chinese names.
            # For languages already present in Google translate, the English
            # names in that engine file are used; Otherwise official names
            # as researched on Wikipedia are used. They're validated against
            # the Chinese names to the best of my ability.
            # Missing "cni", "kbh", "tmh"
            # due to conflict between ISO-639 table and Chinese label
            # one "#" means on iciba but not on google
            "Achinese": "ace",  #
            "Achuar-Shiwiar": "acu",  #
            "Afrikaans": "af",
            "Aguaruna": "agr",  #
            "Akawaio": "ake",  #
            "Albanian": "sq",
            "Amharic": "am",
            "Arabic": "ar",
            "Armenian": "hy",
            "Azerbaijani": "az",
            "Barasana-Eduria": "bsn",  #
            "Bashkir": "ba",  #
            "Basque": "eu",
            "Belarusian": "be",
            "Bemba": "bem",  #
            "Bengali": "bn",
            "Berber": "ber",  #
            "Bislama": "bi",  #
            "Bosnian": "bs",
            "Breton": "br",  #
            "Bulgarian": "bg",
            "Cabécar": "cjp",  #
            "Cantonese": "yue",
            "Catalan": "ca",
            "Cebuano": "ceb",
            "Chamorro": "cha",  #
            "Cherokee": "chr",  #
            "Chichewa": "ny",
            "Chinese (Simplified)": "zh",  # "zh-cn" on Google
            "Chinese (Traditional)": "cht",  # "zh-tw" on Google
            "Chuvash": "cv",
            "Coptic": "cop",  #
            "Corsican": "co",
            "Croatian": "hr",
            "Czech": "cs",
            "Danish": "da",
            "Dhivehi": "dv",  #
            "Dinka": "dik",  #
            "Dutch": "nl",
            "Dzongkha": "dz",  #
            "English": "en",
            "Esperanto": "eo",
            "Estonian": "et",
            "Ewe": "ee",  #
            "Faroese": "fo",  #
            "Fijian": "fj",  #
            "Filipino": "fil",  # "tl" on Google
            "Finnish": "fi",
            "French": "fr",
            "Frisian": "fy",
            "Galela": "gbi",  #
            "Galician": "gl",
            "Ganda": "lg",  #
            "Georgian": "jy",  # "ka" on Google
            "German": "de",
            "Greek": "el",
            "Guerrero Amuzgo": "amu",  #
            "Gujarati": "gu",
            "Haitian Creole": "ht",
            "Hausa": "ha",
            "Hawaiian": "haw",
            "Hebrew": "he",  # "iw" on Google
            "Hindi": "hi",
            "Hmong Daw": "mww",  #
            "Hmong": "hmn",  # not in iciba
            "Hungarian": "hu",
            "Icelandic": "is",
            "Igbo": "ig",
            "Indonesian": "id",
            "Irish": "ga",
            "Italian": "it",
            "Jacalteco": "jac",  #
            "Japanese": "ja",
            "Javanese": "jv",  # "jw" on Google
            "Kabyle": "kab",  #
            "Kannada": "kn",
            "Kaqchikel": "cak",  #
            "Kazakh": "ka",  # Google only has "kk"
            "Kazakh (Cyrillic)": "kk",  # Google has it as just "Kazakh"
            "Kekchí": "kek",  #
            "Khmer": "km",
            "Kinyarwanda": "rw",
            "Kongo": "kg",  #
            "Korean": "ko",
            "Kurdish (Kurmanji)": "ku",
            "Kyrgyz": "ky",
            "Lao": "lo",
            "Latin": "la",
            "Latvian": "lv",
            "Lingala": "ln",  #
            "Lithuanian": "lt",
            "Lukpa": "dop",  #
            "Luxembourgish": "lb",
            "Macedonian": "mk",
            "Malagasy": "mg",
            "Malay": "ms",
            "Malayalam": "ml",
            "Maltese": "mt",
            "Mam": "mam",  #
            "Manx": "gv",  #
            "Maori": "mi",
            "Marathi": "mr",
            "Mari (Eastern)": "mhr",  #
            "Mari (Western)": "mrj",  #
            "Mongolian": "mn",
            "Montenegrin": "me",  #
            "Myanmar (Burmese)": "my",
            "Nahuatl": "nhg",  #
            "Ndyuka": "djk",  #
            "Nepali": "ne",
            "Norwegian": "no",
            "Odia (Oriya)": "or",
            "Ojibwa": "ojb",
            "Oromo": "om",  #
            "Ossetian": "os",  #
            "Paite": "pck",  #
            "Papiamento": "pap",  #
            "Pashto": "ps",
            "Persian": "fa",
            "Polish": "pl",
            "Portuguese": "pt",
            "Potawatomi": "pot",  #
            "Punjabi": "pa",
            "Querétaro Otomi": "otq",  #
            "Quiché": "quc",  #
            "Quichua": "quw",  #
            "Quiotepec Chinantec": "chq",  #
            "Romani": "rmn",  #
            "Romanian": "ro",
            "Rundi": "rn",  #
            "Russian": "ru",
            "Samoan": "sm",
            "Sango": "sg",  #
            "Scots Gaelic": "gd",
            "Serbian": "sr",
            "Seselwa Creole French": "crs",  #
            "Sesotho": "st",
            "Shona": "sn",
            "Shuar": "jiv",  #
            "Sindhi": "sd",
            "Sinhala": "si",
            "Slovak": "sk",
            "Slovenian": "sl",
            "Somali": "so",
            "Spanish": "es",
            "Sundanese": "su",
            "Swahili": "sw",
            "Swedish": "sv",
            "Syriac": "syc",  # considered "extinct" but is somehow supported
            "Tachelhit": "shi",  #
            "Tahitian": "ty",  #
            "Tajik": "tg",
            "Tamil": "ta",
            "Tatar": "tt",
            "Telugu": "te",
            "Tetum": "tet",  #
            "Thai": "th",
            "Tigre": "ti",  #
            "Tiwi": "tw",  #
            "Tok Pisin": "tpi",  #
            "Tonga": "to",  #
            "Tsonga": "ts",
            "Tswana": "tn",  #
            "Turkish": "tr",
            "Turkmen": "tk",
            "Udmurt": "udm",  #
            "Ukrainian": "uk",
            "Uma": "ppk",  #
            "Urdu": "ur",
            "Uspanteco": "usp",  #
            "Uyghur": "uy",  # "ug" on Google
            "Uzbek": "uz",
            "Venda": "ve",  #
            "Vietnamese": "vi",
            "Waray": "war",  #
            "Welsh": "cy",
            "Wolaitta": "wal",  #
            "Wolof": "wol",
            "Xhosa": "xh",
            "Yiddish": "yi",
            "Yoruba": "yo",
            "Yucatán Maya": "yua",  #
            "Zarma": "dje",  #
            "Zulu": "zu",
        }

    async def detect_language(self, text: str):
        return None

    async def get_tts(self, text: str, language: str):
        return None

    async def translate(self, text: str, to_language: str, from_language: str="auto"):
        r = requests.post(
            "https://ifanyi.iciba.com/index.php",
            params={
                "c": "trans",
                "m": "fy",
                "client": "6",
                "auth_user": "key_web_fanyi",
                "sign": (
                    hashlib.md5(
                        ("6key_web_fanyiifanyiweb8hc9s98e" + text).encode("utf-8")
                    ).hexdigest()
                )[0:16],
            },
            data={"from": from_language, "to": to_language, "q": text},
        ).json()

        return {
            "translated-text": r["content"]["out"],
            "source_language": from_language
        }

async def test():
    e = IcibaTranslateEngine()
    print(
        await asyncio.gather(
            e.translate("Hallo", "en", "de"),
            e.translate("Bonjour", "en", "fr"),
            e.translate("Hola", "en", "es"),
        )
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())

