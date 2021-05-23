def get_engine(engine_name, engines, default_engine):
    """
    Returns the corresponding engine for `engine_name` from `engines`, or
    `default_engine` if no corresponding engine is found.
    """
    return next((engine for engine in engines if engine.name == engine_name), default_engine)

def to_full_name(lang_code, engine):
    """
    Returns the full name of `lang_code` from
    `engine.get_supported_languages()` ("auto" can also be passed), or `None`
    if no corresponding name could be found.
    """
    lang_code = lang_code.lower()

    if lang_code == "auto":
        return "Autodetect"

    for key, value in engine.get_supported_languages().items():
        if value.lower() == lang_code:
            return key

    return None

def to_lang_code(lang, engine):
    """
    Returns the corresponding language code of `lang` from
    `engine.get_supported_languages()` (a language code can also be passed,
    which if valid, will be returned as-is). "Autodetect" or "auto" can also be
    passed. If no match could be found, returns `None`.
    """
    lang = lang.lower()

    if lang == "autodetect" or lang == "auto":
        return "auto"

    for key, value in engine.get_supported_languages().items():
        if key.lower() == lang or value.lower() == lang:
            return value

    return None
