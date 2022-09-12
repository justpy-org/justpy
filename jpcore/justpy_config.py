'''
Created on 2022-09-11

@author: wf
'''
from starlette.config import Config

config = Config("justpy.env")
DEBUG = config("DEBUG", cast=bool, default=True)
HOST = config("HOST", cast=str, default="127.0.0.1")
PORT = config("PORT", cast=int, default=8000)
CRASH = config("CRASH", cast=bool, default=False)
LATENCY = config("LATENCY", cast=int, default=0)
if LATENCY:
    print(f"Simulating latency of {LATENCY} ms")
HTML_404_PAGE = "justpy is sorry - that path doesn't exist"