"""
    If something needs configuration, its configuration options are stored in this file

    By Default DEBUG flag is taken from enviroment variable LASTIC_DEBUG, if it is not specified, it is false

"""
from os import getenv
from json import load

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
EXP_TIME = 4 * 60

# Event expire time
EVENT_EXP_TIME = 24 * 3600

# Sentry URL for catching errors
SENTRY_URL = getenv("LASTIC_SENTRY_URL")

# This is methods, that are availible without confirmation token
TOKEN_FREE_METHODS = [
    "/ping",
    "/schema",
    "/robots.txt",
    "/security.txt",
    "/favicon.ico",
    "/push"
]


AVAILABLE_EMOJI = list(load(open("./emojis.json")).keys())

# FCMed endpoints (Should be removed)
FCMED_ENDPOINTS = [
    "/push"
]