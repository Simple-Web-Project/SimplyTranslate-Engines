import aiohttp
import asyncio

def get_engine(engine_name, engines, default_engine):
    """
    Returns the corresponding engine for `engine_name` from `engines`, or
    `default_engine` if no corresponding engine is found.
    """
    return next(
        (engine for engine in engines if engine.name == engine_name), default_engine
    )


async def to_full_name(lang_code, engine, type_="source"):
    """
    Returns the full name of `lang_code` from
    `engine.get_supported_languages()` ("auto" can also be passed), or `None`
    if no corresponding name could be found.
    """
    lang_code = lang_code.lower()

    if lang_code == "auto":
        return "Autodetect"

    supported_langs = None
    if type_ == "source":
        supported_langs = await engine.get_supported_source_languages()
    elif type_ == "target":
        supported_langs = await engine.get_supported_target_languages()

    for key, value in supported_langs.items():
        if value.lower() == lang_code:
            return key

    return None


async def to_lang_code(lang, engine, type_="source"):
    """
    Returns the corresponding language code of `lang` from
    `engine.get_supported_languages()` (a language code can also be passed,
    which if valid, will be returned as-is). "Autodetect" or "auto" can also be
    passed. If no match could be found, returns `None`.
    """
    lang = lang.lower()

    if lang == "autodetect" or lang == "auto":
        return "auto"

    supported_langs = None
    if type_ == "source":
        supported_langs = await engine.get_supported_source_languages()
    elif type_ == "target":
        supported_langs = await engine.get_supported_target_languages()

    for key, value in supported_langs.items():
        if key.lower() == lang or value.lower() == lang:
            return value

    return None

# only the parameters that are ever being used will be added here to avoid clutter
async def async_get(url: str, params={}) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.text()

async def async_post(url: str, headers={}, data="") -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as resp:
            return await resp.text()

