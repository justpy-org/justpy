'''
Created on 2022-09-08

@author: wf
'''
import asyncio
from tests.base_server_test import BaseAsynctest
from tests.browser_test import SeleniumBrowsers
from tests.basetest import Basetest
from examples.basedemo import Demo

class BaseSeleniumTest(BaseAsynctest):
    """
    Base class for Selenium tests
    """
    
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
        
    async def getBrowserForDemo(self):
        """
        get the browser for a Demo test
        """
        browser=SeleniumBrowsers(headless=Basetest.inPublicCI()).getFirst()
        await asyncio.sleep(self.server.sleep_time)
        Demo.testmode = True
        return browser
        