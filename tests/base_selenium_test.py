'''
Created on 2022-09-08

@author: wf
'''
import asyncio
from tests.base_server_test import BaseAsynctest
from tests.basetest import Basetest
from tests.browser_test import SeleniumBrowsers

class BaseSeleniumTest(BaseAsynctest):
    
    async def setUp(
        self, 
        port:int=8123, 
        host:str="127.0.0.1", 
        sleep_time=None, 
        with_server=True, 
        debug=False, 
        profile=True, 
        mode=None):
        await BaseAsynctest.setUp(self, port=port, host=host, sleep_time=sleep_time, with_server=with_server, debug=debug, profile=profile, mode=mode)
        await asyncio.sleep(self.server.sleep_time)
        self.browser = SeleniumBrowsers(headless=Basetest.inPublicCI()).getFirst()