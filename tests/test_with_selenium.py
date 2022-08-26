'''
Created on 2022-08-25

@author: wf
'''
from selenium import webdriver
import justpy as jp

from tests.basetest import BaseAsynctest
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import FirefoxOptions

class TestWithSelenium(BaseAsynctest):
    '''
    testing actual browser behavior with selenium
    '''
    
    async def setUp(self):
        await BaseAsynctest.setUp(self, self.wp_to_test)
        self.firefox_path=GeckoDriverManager().install()
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.browser = webdriver.Firefox(executable_path=self.firefox_path,options=opts)
        

    async def wp_to_test(self):
        '''
        the example Webpage under test
        '''
        wp = jp.WebPage()
        _d=jp.Div(a=wp)
        return wp
    
    async def testHomePage(self):
        '''
        this will actually start a firefox browser and the websocket reload dialog will appear
        '''
        url=self.getUrl("/")
        self.browser.get(url)
        