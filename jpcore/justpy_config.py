'''
Created on 2022-09-11

@author: wf
'''
from starlette.config import Config
import logging
import os
from ssl import PROTOCOL_SSLv23

config = Config("justpy.env")
DEBUG = config("DEBUG", cast=bool, default=True)
HOST = config("HOST", cast=str, default="127.0.0.1")
PORT = config("PORT", cast=int, default=8000)
CRASH = config("CRASH", cast=bool, default=False)
LATENCY = config("LATENCY", cast=int, default=0)
if LATENCY:
    print(f"Simulating latency of {LATENCY} ms")
HTML_404_PAGE = "justpy is sorry - that path doesn't exist"
MEMORY_DEBUG = config("MEMORY_DEBUG", cast=bool, default=False)
SESSIONS = config("SESSIONS", cast=bool, default=True)
SESSION_COOKIE_NAME = config("SESSION_COOKIE_NAME", cast=str, default="jp_token")
SECRET_KEY = config(
    "SECRET_KEY", default="$$$my_secret_string$$$"
)  # Make sure to change when deployed
LOGGING_LEVEL = config("LOGGING_LEVEL", default=logging.WARNING)
UVICORN_LOGGING_LEVEL = config("UVICORN_LOGGING_LEVEL", default="WARNING").lower()
COOKIE_MAX_AGE = config(
    "COOKIE_MAX_AGE", cast=int, default=60 * 60 * 24 * 7
)  # One week in seconds

SSL_VERSION = config("SSL_VERSION", default=PROTOCOL_SSLv23)
SSL_KEYFILE = config("SSL_KEYFILE", default="")
SSL_CERTFILE = config("SSL_CERTFILE", default="")


STATIC_DIRECTORY = config("STATIC_DIRECTORY", cast=str, default=os.getcwd())
STATIC_ROUTE = config("STATIC_MOUNT", cast=str, default="/static")
STATIC_NAME = config("STATIC_NAME", cast=str, default="static")
FAVICON = config(
    "FAVICON", cast=str, default=""
)  # If False gets value from https://elimintz.github.io/favicon.png
TAILWIND = config("TAILWIND", cast=bool, default=True)
QUASAR = config("QUASAR", cast=bool, default=False)
QUASAR_VERSION = config("QUASAR_VERSION", cast=str, default=None)
HIGHCHARTS = config("HIGHCHARTS", cast=bool, default=True)
KATEX = config("KATEX", cast=bool, default=False)
VEGA = config("VEGA", cast=bool, default=False)
BOKEH = config("BOKEH", cast=bool, default=False)
PLOTLY = config("PLOTLY", cast=bool, default=False)
DECKGL = config("DECKGL", cast=bool, default=False)
AGGRID = config("AGGRID", cast=bool, default=True)
AGGRID_ENTERPRISE = config("AGGRID_ENTERPRISE", cast=bool, default=False)

NO_INTERNET = config("NO_INTERNET", cast=bool, default=True)