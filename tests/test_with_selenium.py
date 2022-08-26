'''
Created on 2022-08-25

@author: wf
'''
from selenium import webdriver
import justpy as jp

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
        chrome_options.headless=True
        #self.browser = webdriver.Firefox(executable_path=self.firefox_path,options=opts)
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=chrome_options)


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
        # do not run automatically in CI yet 
        # need to fix 
        if Basetest.inPublicCI():
            return
        url=self.getUrl("/")
        self.browser.get(url)
        