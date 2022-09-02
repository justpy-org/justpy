'''
Created on 2022-08-25

@author: wf
'''

from tests.base_server_test import BaseAsynctest
from tests.browser_test import SeleniumBrowsers
import asyncio
from selenium.webdriver.common.by import By

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
        from examples.tutorial.basic_concepts.hello_world1 import hello_world1
        await super().setUp(hello_world1, port=8125)
        
    async def testHelloWorld1(self):
        '''
        test the hello world 1 example
        '''
        self.browser=SeleniumBrowsers().getFirst()
        await asyncio.sleep(self.sleepTime)
        url=self.getUrl("/")
        self.browser.get(url)
        await asyncio.sleep(self.sleepTime)
        divs=self.browser.find_elements(By.TAG_NAME,"div")
        self.assertEqual(1,len(divs))
        div=divs[0]
        text=div.text
        self.assertEqual("Hello World!",text)
        