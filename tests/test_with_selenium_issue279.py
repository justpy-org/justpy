"""
Created on 2022-08-25

@author: wf
"""
import asyncio
import selenium.common
from selenium.webdriver.common.by import By
from testfixtures import LogCapture
from tests.base_selenium_test import BaseSeleniumTest

class TestIssue279WithSelenium(BaseSeleniumTest):
    """
    testing actual browser behavior with selenium
    """

    async def setUp(self):
        await super().setUp(port=8125)
   
    async def testIssue279(self):
        """
        see https://github.com/justpy-org/justpy/issues/279

        """
        self.browser = await self.getBrowserForDemo()
        from examples.issues.issue_279_key_error import issue_279

        await self.server.start(issue_279)
        url = self.server.get_url("/")
        self.browser.get(url)
        await asyncio.sleep(self.server.sleep_time)
        buttons = self.browser.find_elements(By.TAG_NAME, "button")
        debug = True
        if debug:
            print(f"found {len(buttons)} buttons")
        await asyncio.sleep(0.5)
        ok = "False"
        with LogCapture() as lc:
            try:
                for buttonIndex in [0, 1, 2, 3]:
                    buttons[buttonIndex].click()
                    await asyncio.sleep(0.25)
                await asyncio.sleep(1.0)
                for buttonIndex in [0, 1, 2, 3]:
                    buttons[buttonIndex].click()
                    await asyncio.sleep(0.25)
            except selenium.common.exceptions.StaleElementReferenceException:
                if debug:
                    print(
                        "Expected sideeffect: Selenium already complains about missing button"
                    )
                ok = True
                pass
            await asyncio.sleep(3.2)
            if debug:
                print(f"log capture: {str(lc)}")
            expecteds = [
                "component with id",
                "doesn't exist (anymore ...) it might have been deleted before the event handling was triggered",
            ]
            for i, expected in enumerate(expecteds):
                if not ok:
                    self.assertTrue(expected in str(lc), f"{i}:{expected}")
                else:
                    if not expected in str(lc):
                        print(f"{i}:{expected} missing in captured log")

        self.browser.close()
        await self.server.stop()