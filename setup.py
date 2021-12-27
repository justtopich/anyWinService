# -*- coding: utf-8 -*-
from setuptools import setup


readme = "README.md"

setup(
    name="anyWinService",
    version=__import__("src").__version__,
    url="https://bitbucket.org/JusTopich/anyWinService",
    author="JusTopich",
    py_modules=["anyWinService", "conf", "core"],
    license="GPLv3",
    author_email="alex1.beloglazov@yandex.ru",
    description="Simple service wrapper for Windows applications",
    long_description=open(readme, encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=open("requirements.txt", encoding="utf-8").readlines(),
    keywords=["application", "app", "service", "monitor", "deamon", "windows"],
)
