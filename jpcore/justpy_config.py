'''
Created on 2022-09-11

@author: wf
'''
from starlette.config import Config
import logging
import os
from ssl import PROTOCOL_SSLv23
from jpcore.compat import Compatibility

class JpConfig(Config):
    """
    extended starlette configuration
    """
    # my singleton
    config=None
    
    def __init__(self,env_file=None):
        """
        constructor
        """
        super().__init__(env_file)
        # get the current working directory
        self.cwd=os.getcwd()
        pass
    
    @classmethod
    def reset(cls):
        cls.config=None
        
    @classmethod
    def setup(cls):
        if cls.config is None:
            config=JpConfig("justpy.env")
            cls.config=config
            global DEBUG; DEBUG= config("DEBUG", cast=bool, default=True)
            global VERBOSE; VERBOSE = config("VERBOSE", cast=bool, default=True)
            global HOST; HOST = config("HOST", cast=str, default="127.0.0.1")
            global PORT; PORT = config("PORT", cast=int, default=8000)
            global CRASH; CRASH = config("CRASH", cast=bool, default=False)
            global LATENCY; LATENCY = config("LATENCY", cast=int, default=0)
            if LATENCY and VERBOSE:
                print(f"Simulating latency of {LATENCY} ms")
            global HTML_404_PAGE; HTML_404_PAGE = "justpy is sorry - that path doesn't exist"
            global MEMORY_DEBUG; MEMORY_DEBUG = config("MEMORY_DEBUG", cast=bool, default=False)
            global SESSIONS; SESSIONS = config("SESSIONS", cast=bool, default=True)
            global SESSION_COOKIE_NAME; SESSION_COOKIE_NAME = config("SESSION_COOKIE_NAME", cast=str, default="jp_token")
            global SECRET_KEY; SECRET_KEY = config(
    "SECRET_KEY", default="$$$my_secret_string$$$"
)  # Make sure to change when deployed
            global LOGGING_LEVEL; LOGGING_LEVEL = config("LOGGING_LEVEL", default=logging.WARNING)
            global UVICORN_LOGGING_LEVEL;UVICORN_LOGGING_LEVEL = config("UVICORN_LOGGING_LEVEL", default="WARNING").lower()
            global COOKIE_MAX_AGE; COOKIE_MAX_AGE = config(
    "COOKIE_MAX_AGE", cast=int, default=60 * 60 * 24 * 7
)  # One week in seconds

            global SSL_VERSION; SSL_VERSION = config("SSL_VERSION", default=PROTOCOL_SSLv23)
            global SSL_KEYFILE; SSL_KEYFILE = config("SSL_KEYFILE", default="")
            global SSL_CERTFILE; SSL_CERTFILE = config("SSL_CERTFILE", default="")


            global STATIC_DIRECTORY;STATIC_DIRECTORY = config("STATIC_DIRECTORY", cast=str, default=os.getcwd())
            global STATIC_ROUTE;STATIC_ROUTE = config("STATIC_MOUNT", cast=str, default="/static")
            global STATIC_NAME;STATIC_NAME = config("STATIC_NAME", cast=str, default="static")
            global FAVICON;FAVICON = config(
    "FAVICON", cast=str, default=""
)  # If False gets value from https://elimintz.github.io/favicon.png
            global TAILWIND;TAILWIND = config("TAILWIND", cast=bool, default=True)
            global QUASAR;QUASAR = config("QUASAR", cast=bool, default=False)
            global QUASAR_VERSION;QUASAR_VERSION = config("QUASAR_VERSION", cast=str, default=None)
            global HIGHCHARTS;HIGHCHARTS = config("HIGHCHARTS", cast=bool, default=True)
            global KATEX;KATEX = config("KATEX", cast=bool, default=False)
            global VEGA;VEGA = config("VEGA", cast=bool, default=False)
            global BOKEH;BOKEH = config("BOKEH", cast=bool, default=False)
            global PLOTLY;PLOTLY = config("PLOTLY", cast=bool, default=False)
            global DECKGL;DECKGL = config("DECKGL", cast=bool, default=False)
            global AGGRID;AGGRID = config("AGGRID", cast=bool, default=True)
            global AGGRID_ENTERPRISE;AGGRID_ENTERPRISE = config("AGGRID_ENTERPRISE", cast=bool, default=False)
            global NO_INTERNET;NO_INTERNET = config("NO_INTERNET", cast=bool, default=True)
            global FRONTEND_ENGINE_TYPE;FRONTEND_ENGINE_TYPE = config("FRONTEND_ENGINE_TYPE", cast=str, default="vue")

if Compatibility.version is None:
    JpConfig.setup()