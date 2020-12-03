## dnevnik-mos-ru
[![time tracker](https://wakatime.com/badge/github/IvanProgramming/dnevnik_mos_ru.svg)](https://wakatime.com/badge/github/IvanProgramming/dnevnik_mos_ru)
[![CodeFactor](https://www.codefactor.io/repository/github/ivanprogramming/dnevnik_mos_ru/badge)](https://www.codefactor.io/repository/github/ivanprogramming/dnevnik_mos_ru)

Python библиотека, для удобного доступа к ЭЖД.

##### Пример кода
```python
# Вывод сегодняшних уроков

# Импорт библиотеки
import dnevnik
# Импортируем datetime.datetime для использования функции today()
from datetime import datetime

# Данные для авторизации
LOGIN = ""
PASSWORD = ""

# Авторизуемся
me = dnevnik.Client(LOGIN, PASSWORD)

# Получаем список уроков на сегодня
lessons = me.get_lessons()

# Выводим уроки по порядку
for lesson in lessons:
    print("{0.lesson_number}. {0.subject_name}".format(lesson))
```

##### Установка

- В Linux/MacOS 
    ```
    pip3 install dnevnik-mos-ru
    ``` 
- В Windows
    ```
    pip install dnevnik-mos-ru
    ```
##### Документация API
[Документацию](/docs/API.raml) в формате .RAML можно найти в в папке docs. Можно сгенерировать файл .html с помощью
утилиты [raml2html](https://github.com/raml2html/raml2html)

##### Документация библиотеки
Документацию библиотеки можно будет найти [здесь](https://dnevnik.readthedocs.io/en/latest/). 


