import json
from aiocache import cached


if __name__ != "__main__":
    from .utils import async_post, async_get
else:
    import asyncio
    from utils import async_post, async_get


class LibreTranslateEngine:
    def __init__(self, url, api_key=None):
        self.url = url
        self.api_key = api_key

    name = "libre"
    display_name = "LibreTranslate"

    _supported_languages = None

    async def get_supported_source_languages(self):
        return {"Autodetect": "auto", **await self.get_supported_target_languages()}

    # cache for one week
    @cached(ttl=604800)
    async def get_supported_target_languages(self):
        if self._supported_languages is not None:
            return self._supported_languages

        response = json.loads(await async_get(f"{self.url}/languages"))

        self._supported_languages = {lang["name"]: lang["code"] for lang in response}

        return self._supported_languages

    async def detect_language(self, text: str):
        form = {"q": text}

        if self.api_key is not None:
            form["api_key"] = self.api_key

        response = json.loads(await async_post(f"{self.url}/detect", data=form))

        if type(response) != list:
            return (
                response["error"]
                if "error" in response
                else "odd, something went wrong"
            )

        return max(response, key=lambda item: item["confidence"])["language"]

    async def get_tts(self, text: str, language: str):
        return None

    async def translate(self, text: str, to_language: str, from_language: str="auto"):
        myMap = {}
        form = {"q": text, "source": from_language, "target": to_language}

        if self.api_key is not None:
            form["api_key"] = self.api_key

        response_text = await async_post(f"{self.url}/translate", data=form)

        response = json.loads(response_text)
        if "translatedText" in response:
            translated_text = response["translatedText"]
        elif "error" in response:
            translated_text = response["error"]
        else:
            translated_text = "odd, something went wrong"
        return {
            "translated-text": translated_text,
            "source_language": from_language
        }


async def test():
    e = LibreTranslateEngine("https://libretranslate.de")
    print(
        await asyncio.gather(
            e.translate("Hallo", "en", "de"),
            e.translate("Bonjour", "en", "fr"),
            e.translate("Hola", "en", "es"),
        )
    )

    print(await e.detect_language("Rechtsanwalt"))
    print(await e.get_supported_source_languages())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
