'''
Created on 2022-09-14

@author: wf
'''
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.base_selenium_test import BaseSeleniumTest

class TestDatabaseExample(BaseSeleniumTest):
    """
    testing database example
    """

    async def setUp(self):
        await super().setUp(port=8127)
        
    def findElement(self,condition,timeout=4.0):
        element_present = EC.presence_of_element_located(condition)
        element=WebDriverWait(self.browser, timeout).until(element_present)
        return element
        
    async def testDatabaseExample(self):
        """
        test database example from grids_tutorial/database.md
        """
        self.browser = await self.getBrowserForDemo()
        from examples.tutorial.db_test import db_test
        await self.server.start(db_test)
        url = self.server.get_url("/")
        self.browser.get(url)
        await asyncio.sleep(self.server.sleep_time)
        
        selectInput=self.findElement((By.CLASS_NAME,"q-select__autocomplete-input"))
        #select=Select(selectElement)
        #select.selectByIndex(2)
        #selectInput.clear()
        #selectInput.send_keys("artists")
        await asyncio.sleep(3)
        self.browser.close()
        await asyncio.sleep(self.server.sleep_time)
        await self.server.stop()