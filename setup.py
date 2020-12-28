from setuptools import setup, find_packages
from dnevnik import __version__

setup(
    name='dnevnik-mos-ru',
    version=__version__,
    description="This package is kind of wrapper for dnevnik.mos.ru API service",
    url='https://github.com/IvanProgramming/dnevnik_mos_ru',
    author='Ivan Vlasov',
    packages=find_packages(),
    install_requires=[
        'requests',
        'selenium'
    ]
)
