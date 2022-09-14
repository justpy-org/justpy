'''
Created on 2022-09-14

@author: wf
'''
import asyncio
from selenium.webdriver.common.by import By
from tests.base_selenium_test import BaseSeleniumTest
from jpcore.webpage import WebPage

class TestAjaxWithSelenium(BaseSeleniumTest):
    """
    testing ajax (non-websocket) behavior
    """

    async def setUp(self):
        await super().setUp(port=8126)
        
    async def testAjax(self):
        """
        test ajax (non-websocket behavior) according to tutorial
        """
        WebPage.use_websockets=False
        self.browser = await self.getBrowserForDemo()
        from examples.tutorial.ajax.hello_test import hello_test
        await self.server.start(hello_test,websockets=False)
        url = self.server.get_url("/")
        self.browser.get(url)
        await asyncio.sleep(self.server.sleep_time)
        divs = self.browser.find_elements(By.TAG_NAME, "div")
        for div in divs:
            div.click()
            await asyncio.sleep(0.1)
        await asyncio.sleep(self.server.sleep_time)
        #debug=self.debug
        debug=True
        for div in divs:
            if debug:
                print(div.text)
            self.assertTrue(f"was clicked 1 times" in div.text)
        self.browser.close()
        await asyncio.sleep(self.server.sleep_time)
        await self.server.stop()