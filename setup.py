from setuptools import setup

from dnevnik import __version__

setup(
    name='my_pip_package',
    version=__version__,
    url='https://github.com/IvanProgramming/dnevnik_mos_ru',
    author='Ivan Vlasov',
    py_modules=['dnevnik'],
)
