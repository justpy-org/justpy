'''
Created on 2022-08-25

@author: wf
'''

from tests.base_server_test import BaseAsynctest
from tests.browser_test import SeleniumBrowsers
import asyncio
from selenium.webdriver.common.by import By
from tests.basetest import Basetest

class TestTutorial(BaseAsynctest):
    '''
    test tutorial examples
    '''
    
    async def setUp(self):
        '''
        prepare justpy tutorial app
        '''
        from examples.basedemo import Demo
        Demo.testmode=True
        await super().setUp(port=8125)
        self.browser=SeleniumBrowsers(headless=Basetest.inPublicCI()).getFirst()
        await asyncio.sleep(self.sleepTime)
        
    async def getElements(self,server,wpfunc,tagName:str="div"):
        await server.start(wpfunc)
        url=server.getUrl("/")
        self.browser.get(url)
        await asyncio.sleep(self.sleepTime)
        divs=self.browser.find_elements(By.TAG_NAME,tagName)
        return divs
        
    async def testHelloWorld1(self):
        '''
        test the hello world 1 example
        '''
        from examples.tutorial.basic_concepts.hello_world1 import hello_world1
        divs=await self.getElements(self.server,hello_world1,"div")
        self.assertEqual(1,len(divs))
        div=divs[0]
        text=div.text
        self.assertEqual("Hello World!",text)
        
    async def testHelloWorld2(self):
        '''
        test the hello world 2 example
        '''
        from examples.tutorial.basic_concepts.hello_world2 import hello_world2
        server=self.server.nextServer()
        divs=await self.getElements(server,hello_world2,"p")
        self.assertEqual(10,len(divs))
        await server.stop()
        