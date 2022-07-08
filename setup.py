from setuptools import setup

setup(
    name = "simplytranslate_engines",
    version = "0.0.3",
    url = "https://codeberg.org/SimpleWeb/SimplyTranslate-Engines",

    license = "AGPLv3 or later",
    keywords = "translation",
    packages = ["simplytranslate_engines"],
    install_requires = [
        "lxml",
        "requests",
        "translatepy",
        # Currently, pip defaults to a broken alpha release from 2019.
        # Requiring <4 forces the installation of the correct, stable package.
        # see https://codeberg.org/SimpleWeb/SimplyTranslate-Docker/issues/1
        "aiohttp<4",
        "aiocache"
    ]
)
