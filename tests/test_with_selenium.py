'''
Created on 2022-08-25

@author: wf
'''
from selenium import webdriver
import justpy as jp
import time

from tests.basetest import BaseAsynctest, Basetest
#from webdriver_manager.firefox import GeckoDriverManager
#from selenium.webdriver import FirefoxOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class TestWithSelenium(BaseAsynctest):
    '''
    testing actual browser behavior with selenium
    '''
    
    async def setUp(self):
        await BaseAsynctest.setUp(self, self.wp_to_test)
        
        #self.firefox_path=GeckoDriverManager().install()
        #opts = FirefoxOptions()
        chrome_options = Options()
        chrome_options.headless=Basetest.inPublicCI()
        #self.browser = webdriver.Firefox(executable_path=self.firefox_path,options=opts)
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=chrome_options)


    async def onDivClick(self, msg):
        print(msg)
        self.clickCount+=1
        self.text= f'I was clicked {self.clickCount} times'
        wp = msg.page
        await wp.update()
    
    async def wp_to_test(self):
        '''
        the example Webpage under test
        '''
        wp = jp.WebPage()
        self.clickCount=0
        d = jp.Div(text='Not clicked yet', a=wp, classes='w-48 text-xl m-2 p-1 bg-blue-500 text-white')
        d.on('click', self.onDivClick)
        d.additional_properties =['screenX', 'pageY','altKey','which','movementX','button', 'buttons']
        return wp
    
    async def testHomePage(self):
        '''
        this will actually start a firefox browser and the websocket reload dialog will appear
        '''
        # do not run automatically in CI yet 
        # need to fix 
        if Basetest.inPublicCI():
            return
        url=self.getUrl("/")
        self.browser.get(url)
        time.sleep(1000)
        