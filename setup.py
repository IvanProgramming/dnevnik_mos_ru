from setuptools import setup, find_packages

from dnevnik import __version__

setup(
    name='dnevnik-mos-ru',
    version=__version__,
    url='https://github.com/IvanProgramming/dnevnik_mos_ru',
    author='Ivan Vlasov',
    py_modules=["dnevnik"],
    install_requires=[
        'requests',
    ]
)
