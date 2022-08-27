'''
Created on 2022-08-25

@author: wf
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
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
        sleepTime=0.2
        time.sleep(sleepTime)
        divs=self.browser.find_elements(By.TAG_NAME,"div")
        # get the clickable div
        div=divs[1]
        self.assertEqual("Not clicked yet",div.text)
        for i in range(5):
            div.click()
            time.sleep(sleepTime)
            self.assertEqual(f"I was clicked {i+1} times",div.text)
        time.sleep(2)
        