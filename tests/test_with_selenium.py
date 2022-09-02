'''
Created on 2022-08-25

@author: wf
'''
import asyncio
from selenium.webdriver.common.by import By
import justpy as jp
from tests.browser_test import SeleniumBrowsers
from tests.base_server_test import BaseAsynctest
from tests.basetest import Basetest

class TestWithSelenium(BaseAsynctest):
    '''
    testing actual browser behavior with selenium
    '''
    
    async def setUp(self):
        await super().setUp(port=8124)

    async def onDivClick(self, msg):
        '''
        handle the click of the div
        '''
        print(msg)
        self.clickCount+=1
        msg.target.text= f'I was clicked {self.clickCount} times'
     
    async def wp_to_test(self):
        '''
        the example Webpage under test
        '''
        wp = jp.WebPage(debug=True)
        self.clickCount=0
        d = jp.Div(text='Not clicked yet', a=wp, classes='w-48 text-xl m-2 p-1 bg-blue-500 text-white')
        d.on('click', self.onDivClick)
        d.additional_properties =['screenX', 'pageY','altKey','which','movementX','button', 'buttons']
        return wp
    
    async def testClickDemo(self):
        '''
        this will actually start a firefox browser and the websocket reload dialog will appear
        '''
        # do not run automatically in CI yet 
        # need to fix 
        #if Basetest.inPublicCI():
        #    return
        self.browser=SeleniumBrowsers(headless=Basetest.inPublicCI()).getFirst()
        await asyncio.sleep(self.server.sleepTime)
        await self.server.start(self.wp_to_test)
        url=self.server.getUrl("/")
        self.browser.get(url)
        await asyncio.sleep(self.server.sleepTime)
        divs=self.browser.find_elements(By.TAG_NAME,"div")
        # get the clickable div
        div=divs[1]
        self.assertEqual("Not clicked yet",div.text)
        for i in range(5):
            div.click()
            await asyncio.sleep(self.server.sleepTime)
            self.assertEqual(f"I was clicked {i+1} times",div.text)
        self.browser.close()
        await asyncio.sleep(self.server.sleepTime)
        