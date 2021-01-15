## dnevnik-mos-ru
[![time tracker](https://wakatime.com/badge/github/IvanProgramming/dnevnik_mos_ru.svg)](https://wakatime.com/badge/github/IvanProgramming/dnevnik_mos_ru)
[![CodeFactor](https://www.codefactor.io/repository/github/ivanprogramming/dnevnik_mos_ru/badge)](https://www.codefactor.io/repository/github/ivanprogramming/dnevnik_mos_ru)
[![](https://tokei.rs/b1/github/XAMPPRocky/tokei)](https://github.com/IvanProgramming/dnevnik_mos_ru)
[![Discord](https://discord.gg/qMUVFTXRcM)](https://img.shields.io/discord/799693120358711356)
![GitHub Repo stars](https://img.shields.io/github/stars/IvanProgramming/dnevnik_mos_ru?style=social)

Python библиотека, для удобного доступа к ЭЖД.

##### Пример кода
```python
# Вывод сегодняшних уроков
# Импорт библиотеки
import dnevnik

# Данные для авторизации
LOGIN = ""
PASSWORD = ""

# Данные для Selenium
DRIVER_PATH = ""

# Авторизуемся
me = dnevnik.Client(login=LOGIN, password=PASSWORD, use_selenium=True, selenium_executable_path=DRIVER_PATH)

# Получаем список уроков на сегодня
lessons = me.get_lessons()

# Выводим уроки по порядку
for lesson in lessons:
    print("{0.lesson_number}. {0.subject_name}".format(lesson))
```
#### Установка

###### Установка Selenium
Пока реализован только вариант с ChromeDriver.
1. Зайти в Google Chrome. Три точки сверху -> Справка -> О браузуре Google Chrome
2. Запомнить версию.
3. [Отсюда](https://chromedriver.chromium.org/) скачать chromedriver для своей версии Chrome и своей OS
4. Скопируйте исполняемый файл в какую-нибудь папку и запомните путь.
5. В конструкторе Client параметр флаг use_selenium и внесите путь в selenium_executable_path

###### Установка библиотеки

- В Linux/MacOS 
    ```
    pip3 install dnevnik-mos-ru
    ``` 
- В Windows
    ```
    pip install dnevnik-mos-ru
    ``` 
 
##### Документация API
[Документацию API](/docs/API.raml) в формате .RAML можно найти в в папке docs. Можно сгенерировать файл .HTML с помощью
утилиты [raml2html](https://github.com/raml2html/raml2html)

##### Документация библиотеки
Документацию библиотеки можно будет найти [здесь](https://dnevnik.readthedocs.io/en/latest/). 

##### Join [Discord Server](https://discord.gg/qMUVFTXRcM)

