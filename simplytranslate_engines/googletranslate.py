import lxml.html as lxml
from urllib.parse import urlencode, quote, urlparse, parse_qs
import json
import re
from aiocache import cached

if __name__ != "__main__":
    from .utils import async_get, async_post
else:
    import asyncio
    from utils import async_get, async_post


class GoogleTranslateEngine:
    name = "google"
    display_name = "Google"

    async def _get_langs_from_google(self, **kwargs):
        if kwargs["type"] == "source":
            langs_type = "sl"
        elif kwargs["type"] == "target":
            langs_type = "tl"
        else:
            raise ArgumentError(
                f"`type` must be either `source` or `target`, but {kwargs['type']} was passed"
            )

        doc = lxml.fromstring(
            await async_get(
                "https://translate.google.com/m",
                params={"sl": "en", "tl": "en", "mui": langs_type, "hl": "en-US"},
            )
        )

        return {
            # Language code: language name
            parse_qs(urlparse(item.find("a").get("href")).query)[langs_type][
                0
            ]: item.find("a").text_content()
            for item in doc.find_class("language-item")
        }

    # Cache for one week.
    @cached(ttl=604800)
    async def get_supported_source_languages(self):
        langs = await self._get_langs_from_google(type="source")

        # It's originally "Detect language," but this is what we use.
        langs["auto"] = "Autodetect"

        # It's originally "Chinese", but this is clearer.
        langs["zh-CN"] = "Chinese (Simplified)"

        return {lang_name: lang_code for lang_code, lang_name in langs.items()}

    # Cache for one week.
    @cached(ttl=604800)
    async def get_supported_target_languages(self):
        return {
            lang_name: lang_code
            for lang_code, lang_name in (
                await self._get_langs_from_google(type="target")
            ).items()
        }

    async def detect_language(self, text: str):
        return None

    async def get_tts(self, text: str, language: str):
        if text == None or language == None:
            return None
        elif len(text) == 0 or len(language) == 0:
            return None

        if language == "auto":
            language = "en"

        params = urlencode({"tl": language, "q": text.strip(), "client": "tw-ob"})
        return f"https://translate.google.com/translate_tts?{params}"

    async def translate(self, text: str, to_language: str, from_language: str="auto"):
        my_map = {}
        try:
            url = "https://translate.google.com/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&rt=c"

            req = json.dumps([[text, from_language, to_language, True], [None]])
            req = [[["MkEWBc", req, None, "generic"]]]
            req = "f.req=" + quote(json.dumps(req))  # URL encode this

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
                    if definition_type is None:
                        definition_type = "unknown"
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
                        if translation_type is None:
                            translation_type = "unknown"
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

        my_map["source_language"] = from_language

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
