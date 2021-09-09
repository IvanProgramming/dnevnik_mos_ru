from setuptools import setup, find_packages
from dnevnik import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='dnevnik-mos-ru',
    version=__version__,
    description="This package is kind of wrapper for dnevnik.mos.ru API service",
    long_description_content_type="text/markdown",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/IvanProgramming/dnevnik_mos_ru',
    project_urls={
        "Bug Tracker": "https://github.com/IvanProgramming/dnevnik_mos_ru/issues",
    },
    author='Ivan',
    packages=find_packages(),
    install_requires=[
        'requests',
        'selenium',
        'bs4',
        'lxml',
        'pydantic',
        'Inject'
    ]
)
