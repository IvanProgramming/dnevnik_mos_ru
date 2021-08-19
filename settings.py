"""
    If something needs configuration, its configuration options are stored in this file

    By Default DEBUG flag is taken from enviroment variable LASTIC_DEBUG, if it is not specified, it is false

"""
from os import getenv

DEBUG = getenv("LASTIC_DEBUG") == "true"

# Development
if DEBUG:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost", "lastic.prbla.ru"]
    REQUIRE_HTTPS = False

# Production
else:
    ALLOWED_HOSTS = ["lastic.prbla.ru"]
    REQUIRE_HTTPS = True

DB_URL = "mongodb://localhost:27017"

# Expire time sets in seconds
EXP_TIME = 30
