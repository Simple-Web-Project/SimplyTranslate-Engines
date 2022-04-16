from setuptools import setup

setup(
    name = "simplytranslate_engines",
    version = "0.0.1",
    url = "https://codeberg.org/SimpleWeb/SimplyTranslate-Engines",

    license = "AGPLv3 or later",
    keywords = "translation",
    packages = ["simplytranslate_engines"],
    install_requires = [
        "lxml",
        "requests",
        "translatepy"
    ]
)
