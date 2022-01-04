import lxml.html as lxml
from urllib.parse import urlencode
import requests
import json

class GoogleTranslateEngine:
    name = "google"
    display_name = "Google"

    def get_supported_languages(self):
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

        params = urlencode({
            "tl": language,
            "q": text.strip(),
            "client": "tw-ob"
        })
        return f"https://translate.google.com/translate_tts?{params}"

    """
    It turns out that the googleapis.com domain is being rate-limited which becomes problematic on large instances, because of that we use the "old" way
    of fetching the translation using the mobile page

    def translate(self, text, to_language, from_language="auto"):
        r = requests.get(
            "https://translate.googleapis.com/translate_a/single?dt=bd&dt=ex&dt=ld&dt=md&dt=rw&dt=rm&dt=ss&dt=t&dt=at&dt=qc",
            params={
                "client": "gtx", # client
                "ie": "UTF-8", # input encoding
                "oe": "UTF-8", # output encoding
                "sl": from_language,
                "tl": to_language,
                "hl": to_language,
                "q": text
            }
        )

        try:
            j = json.loads(r.text)

            request_body = j[0]
            translation = ""

            for i in range(len(request_body)):
                if request_body[i][0] != None:
                    translation += request_body[i][0]

            return translation

            # This will probably be used in a future version
            #definition_body = request_body[1][0]
        except Exception as e:
            print("Error translating using Google Translate:")
            print(str(e))
            pass

        return ""
    """"

    def translate(self, text, to_language, from_language="auto"):
        r = requests.get(
            "https://translate.google.com/m",
            params = {
                "tl": to_language,
                "hl": to_language,
                "q": text
            }
        )

        doc = lxml.fromstring(r.text)
        for container in doc.find_class("result-container"):
            return container.text_content()

        return ""



if __name__ == "__main__":
    print(GoogleTranslateEngine().translate("Hello Weird World!!\n\n\nHi!", "fr", "en"))
