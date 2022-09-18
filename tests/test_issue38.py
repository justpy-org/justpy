"""
Created on 2022-09-17

@author: th
"""
import asyncio
import unittest

from selenium.webdriver.common.by import By
import justpy as jp
from tests.base_selenium_test import BaseSeleniumTest



@unittest.skipIf(True, "Issue occurs allways since it is the cause on type conversions")
class TestIssue38(BaseSeleniumTest):
    """
    testing issue 38
    https://github.com/justpy-org/justpy/issues/38
    """

    async def setUp(self):
        await BaseSeleniumTest.setUp(self,port=8124)

    async def tearDown(self):
        self.browser.close()
        await asyncio.sleep(self.server.sleep_time)
        await self.server.stop()

    def my_input3(self, msg):
        value = self.in1.value
        print(value)
        self.div.text = self.in1.value

    def input_demo4(self, request):
        input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 " \
                        "focus:outline-none focus:bg-white focus:border-purple-500 "
        p_classes = 'm-2 p-2 h-32 text-xl border-2'
        wp = jp.WebPage()
        self.in1 = jp.Input(name="inputField", type='number', a=wp, classes=input_classes, placeholder='Please type here')
        self.div = jp.Div(name="displayDiv", text='What you type will show up here', classes=p_classes, a=wp)
        self.in1.on('change', self.my_input3)
        return wp

    async def test_issue_38(self):
        """
        test when the issue occurs that input and input display differ
        """
        await self.server.start(self.input_demo4)
        url = self.server.get_url("/")
        self.browser.get(url)
        await asyncio.sleep(self.server.sleep_time)
        input_field = self.browser.find_elements(By.NAME, "inputField")[0]
        display_div = self.browser.find_elements(By.NAME, "displayDiv")[0]
        value = ""
        for i in range(1,20):
            value += "1"
            input_field.send_keys("1")
            display_div.click()  # lose focus
            await asyncio.sleep(self.server.sleep_time)
            self.assertEqual(value, display_div.text, f"After {i} numbers the issue occurs")
