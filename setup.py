from setuptools import setup

setup(
    name = "simplytranslate_engines",
    version = "0.0.1",
    url = "https://git.sr.ht/~metalune/simplynews_engines",

    license = "AGPLv3 or later",
    keywords = "translation",
    packages = ["simplytranslate_engines"],
    install_requires = [
        "lxml",
        "requests"
    ]
)
