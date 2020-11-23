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
PROFILE_ID = 0000000
AUTH_TOKEN = "token"

# Авторизуемся
me = dnevnik.Client(AUTH_TOKEN, PROFILE_ID)

# Получаем список уроков на сегодня
lessons = me.get_lessons(date_from=datetime.today(), date_to=datetime.today())

# Выводим уроки по порядку
for lesson in lessons:
    print("{0.ordinal_number}. {0.subject_name}".format(lesson))
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
##### Получение токена
Руководство по получению токена можно найти [здесь](/docs/auth_token.md)
