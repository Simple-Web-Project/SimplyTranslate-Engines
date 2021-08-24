import lxml.html as lxml
import requests

class GoogleTranslateEngine:
    name = "google"

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

    def translate(self, text, to_language, from_language="auto"):
        r = requests.get(
            "https://translate.google.com/m",
            params={
                "q": text,
                "sl": from_language,
                "tl": to_language
            })

        doc = lxml.fromstring(r.text)
        for container in doc.find_class("result-container"):
            return container.text_content()

        return ""

if __name__ == "__main__":
    print(GoogleTranslateEngine().translate("hello", "fr", "en"))
