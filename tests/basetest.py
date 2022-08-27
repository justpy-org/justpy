'''
Created on 2021-08-19

@author: wf
'''
import justpy as jp
import aiohttp
import asynctest
import asyncio
import os
import getpass
from unittest import TestCase
import time
from threading import Thread

class BaseAsynctest(asynctest.TestCase):
    '''
    basic asynch test
    '''
    # https://github.com/encode/starlette/blob/master/docs/testclient.md
    # https://stackoverflow.com/questions/57412825/how-to-start-a-uvicorn-fastapi-in-background-when-testing-with-pytest
    # https://github.com/encode/uvicorn/discussions/1103
    # https://stackoverflow.com/questions/68603658/how-to-terminate-a-uvicorn-fastapi-application-cleanly-with-workers-2-when

    async def setUp(self,wpfunc,port:int=8123,host:str="127.0.0.1",sleepTime=0.2,debug=False,profile=True):
        """ Bring server up. 
        
        Args:
            wpfunc: the (async) function for the webpage
            port(int): the port
            host(str): the host 
            sleepTime(float): the time to sleep after server process was started
            debug(bool): if True debugging is on
            profile(bool): if True time for test is profiled
        """ 
        self.port=port
        self.host=host
        self.debug=debug
        self.profile=profile
        msg=f"test {self._testMethodName}, debug={self.debug}"
        self.profiler=Profiler(msg,profile=self.profile)
        self.thread = Thread(target=jp.justpy,
                            args=(wpfunc,),
                            kwargs={
                                "host": self.host,
                                "port": self.port,
                            },
                            daemon=True)
        self.thread.start()
        await asyncio.sleep(sleepTime)  # time for the server to start
        
    async def tearDown(self):
        """ Shutdown the app. """
        #self.proc.terminate()
        self.profiler.time()
        
    def getUrl(self,path):
        '''
        get the url for the given path
        
        Args:
            path(str): the path
        Returns:
            str: the url for the path
        
        '''
        url=f"http://{self.host}:{self.port}{path}"
        return url
        
    async def getResponseHtml(self,path:str="/"):
        '''
        get the status and raw html for the given path
        
        Args:
            path(str): the path
        Returns:
            status,rawhtml
        '''
        async with aiohttp.ClientSession() as session:
            url=self.getUrl(path)
            async with session.get(url) as resp:
                rawhtml = await resp.content.read()
                status = resp.status
        return status,rawhtml
                

class Basetest(TestCase):
    '''
    base test case
    '''
    
    def setUp(self,debug=False,profile=True):
        '''
        setUp test environment
        '''
        TestCase.setUp(self)
        self.debug=debug
        self.profile=profile
        msg=f"test {self._testMethodName}, debug={self.debug}"
        self.profiler=Profiler(msg,profile=self.profile)
        
    def tearDown(self):
        TestCase.tearDown(self)
        self.profiler.time()

    @staticmethod
    def inPublicCI():
        '''
        are we running in a public Continuous Integration Environment?
        '''
        publicCI = getpass.getuser() in ["travis", "runner"]
        jenkins = "JENKINS_HOME" in os.environ
        return publicCI or jenkins

    @staticmethod
    def isUser(name:str):
        """Checks if the system has the given name"""
        return getpass.getuser() == name

class Profiler:
    '''
    simple profiler
    '''
    def __init__(self,msg,profile=True):
        '''
        construct me with the given msg and profile active flag
        
        Args:
            msg(str): the message to show if profiling is active
            profile(bool): True if messages should be shown
        '''
        self.msg=msg
        self.profile=profile
        self.starttime=time.time()
        if profile:
            print(f"Starting {msg} ...")
    
    def time(self,extraMsg=""):
        '''
        time the action and print if profile is active
        '''
        elapsed=time.time()-self.starttime
        if self.profile:
            print(f"{self.msg}{extraMsg} took {elapsed:5.1f} s")
        return elapsed