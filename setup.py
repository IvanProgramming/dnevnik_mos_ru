from setuptools import setup, find_packages

setup(
    name='dnevnik-mos-ru',
    version="0.0.3 Alpha",
    url='https://github.com/IvanProgramming/dnevnik_mos_ru',
    author='Ivan Vlasov',
    py_modules=["dnevnik"],
    install_requires=[
        'requests',
    ]
)
