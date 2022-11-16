'''
Created on 2022-09-11

@author: wf
'''
from jpcore.compat import Compatibility
import jpcore.jpconfig as jpconfig
from starlette.config import Config
import logging
import os
from ssl import PROTOCOL_SSLv23
from starlette.config import environ

class JpConfig(Config):
    """
    extended starlette configuration see https://www.starlette.io/config/
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
    def set(cls,key:str,value:object):
        """
        set a config value
        
        Args:
            str(key): the name of the config setting to modify
            value(object): the value to set the config setting to
        """
        environ[key]=value
    
    @classmethod
    def reset(cls):
        cls.config=None
        
    @classmethod
    def setup(cls):
        if cls.config is None:
            config=JpConfig("justpy.env")
            cls.config=config
            jpconfig.DEBUG= config("DEBUG", cast=bool, default=True)
            jpconfig.VERBOSE = config("VERBOSE", cast=bool, default=True)
            jpconfig.HOST = config("HOST", cast=str, default="127.0.0.1")
            jpconfig.PORT = config("PORT", cast=int, default=8000)
            jpconfig.CRASH = config("CRASH", cast=bool, default=False)
            jpconfig.LATENCY = config("LATENCY", cast=int, default=0)
            if jpconfig.LATENCY and jpconfig.VERBOSE:
                print(f"Simulating latency of {jpconfig.LATENCY} ms")
            jpconfig.HTML_404_PAGE = "justpy is sorry - that path doesn't exist"
            jpconfig.MEMORY_DEBUG = config("MEMORY_DEBUG", cast=bool, default=False)
            jpconfig.SESSIONS = config("SESSIONS", cast=bool, default=True)
            jpconfig.SESSION_COOKIE_NAME = config("SESSION_COOKIE_NAME", cast=str, default="jp_token")
            jpconfig.SECRET_KEY = config(
    "SECRET_KEY", default="$$$my_secret_string$$$"
)  # Make sure to change when deployed
            jpconfig.LOGGING_LEVEL = config("LOGGING_LEVEL", default=logging.WARNING)
            jpconfig.UVICORN_LOGGING_LEVEL = config("UVICORN_LOGGING_LEVEL", default="WARNING").lower()
            jpconfig.COOKIE_MAX_AGE = config(
    "COOKIE_MAX_AGE", cast=int, default=60 * 60 * 24 * 7
)  # One week in seconds

            jpconfig.SSL_VERSION = config("SSL_VERSION", default=PROTOCOL_SSLv23)
            jpconfig.SSL_KEYFILE = config("SSL_KEYFILE", default="")
            jpconfig.SSL_CERTFILE = config("SSL_CERTFILE", default="")

            jpconfig.STATIC_DIRECTORY = config("STATIC_DIRECTORY", cast=str, default=os.getcwd())
            jpconfig.STATIC_ROUTE = config("STATIC_MOUNT", cast=str, default="/static")
            jpconfig.STATIC_NAME = config("STATIC_NAME", cast=str, default="static")
            jpconfig.FAVICON = config(
    "FAVICON", cast=str, default=""
)  # If False gets value from https://elimintz.github.io/favicon.png
            jpconfig.TAILWIND = config("TAILWIND", cast=bool, default=True)
            jpconfig.QUASAR = config("QUASAR", cast=bool, default=False)
            jpconfig.QUASAR_VERSION = config("QUASAR_VERSION", cast=str, default=None)
            jpconfig.HIGHCHARTS = config("HIGHCHARTS", cast=bool, default=True)
            jpconfig.KATEX = config("KATEX", cast=bool, default=False)
            jpconfig.VEGA = config("VEGA", cast=bool, default=False)
            jpconfig.BOKEH = config("BOKEH", cast=bool, default=False)
            jpconfig.PLOTLY = config("PLOTLY", cast=bool, default=False)
            jpconfig.DECKGL = config("DECKGL", cast=bool, default=False)
            jpconfig.AGGRID = config("AGGRID", cast=bool, default=True)
            jpconfig.AGGRID_ENTERPRISE= config("AGGRID_ENTERPRISE", cast=bool, default=False)
            jpconfig.NO_INTERNET= config("NO_INTERNET", cast=bool, default=True)
            jpconfig.FRONTEND_ENGINE_TYPE = config("FRONTEND_ENGINE_TYPE", cast=str, default="vue")


if Compatibility.version is None:
    JpConfig.setup()