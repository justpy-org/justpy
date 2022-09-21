"""
Created on 2022-09-17

@author: th
"""
import asyncio
import unittest

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import justpy as jp
from tests.base_selenium_test import BaseSeleniumTest


@unittest.skipIf(True, "A fix was proposed activate once applied")
class TestIssue150(BaseSeleniumTest):
    """
    testing issue 150
    https://github.com/justpy-org/justpy/issues/150
    """

    async def setUp(self):
        await BaseSeleniumTest.setUp(self,port=8124)

    async def tearDown(self):
        self.browser.close()
        await asyncio.sleep(self.server.sleep_time)
        await self.server.stop()

    def issue_page(self):
        """
        webpage containing the issue
        """
        wp = jp.QuasarPage()
        self.date_field = QInputDateTime(
                filled=True,
                style='width: 600px',
                a=wp,
                classes="q-pa-md",
                value='2022-05-01 18:44',
                name="date_field"
        )
        return wp

    async def test_issue_150(self):
        """
        tests the presence of issue 150
        When selecting a new date through the date picker an infinite event loop is started.
        Cause found and documented in the issue.
        """
        await self.server.start(self.issue_page)
        url = self.server.get_url("/")
        self.browser.get(url)
        driver = self.get_waiting_browser(self.browser)
        input_field = self.browser.find_elements(By.TAG_NAME, "i")[0]
        input_field.click()
        day_fields_locator = (By.CLASS_NAME, "q-date__calendar-item")
        driver.until(EC.element_to_be_clickable(day_fields_locator))
        day_fields = self.browser.find_elements(*day_fields_locator)
        day_fields[20].click()
        click_count_locator = (By.NAME, "count_date_changes")
        # check that the click was registered
        self.assertTrue(
                driver.until(
                        EC.text_to_be_present_in_element(
                                locator=click_count_locator,
                                text_="1")))
        # check that the infinite loop does not start → count_date_changes should not change its value
        self.assertRaises(
                TimeoutException,
                lambda: driver.until_not(
                        EC.text_to_be_present_in_element(locator=click_count_locator, text_="1")))

    @unittest.skipIf(True, "Only for manual testing")
    def test_manual(self):
        """
        start the server to test the issue manually
        """
        jp.justpy(self.issue_page, port=8500)


class QInputDateTime(jp.QInput):
    """
    component to test
    see https://github.com/justpy-org/justpy/issues/150
    """

    def __init__(self, **kwargs):
        """
        constructor
        """
        super().__init__(**kwargs)
        self.mask = '####-##-## ##:##'

        # date selection
        date_slot = jp.QIcon(name='event', classes='cursor-pointer')
        c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=date_slot)
        locale = {
            'days': 'Neděle_Pondělí_Úterý_Středa_Čtvrtek_Pátek_Sobota'.split('_'),
            'daysShort': 'Ne_Po_Út_St_Čt_Pá_So'.split('_'),
            'months': 'Leden_Únor_Březen_Duben_Květen_Červen_Červenec_Srpen_Září_Říjen_Listopad_Prosinec'.split('_'),
            'monthsShort': 'Led_Úno_Bře_Dub_Kvě_Čvn_Čvc_Srp_Zář_Říj_Lis_Pro'.split('_')
        }
        self.date = jp.QDate(
                mask='YYYY-MM-DD HH:mm',
                name='date_popup',
                a=c2,
                locale=locale
        )
        self.date.parent = self
        self.date.value = self.value
        self.date.on('input', self.date_time_change)
        self.prepend_slot = date_slot

        # time selection
        time_slot = jp.QIcon(name='access_time', classes='cursor-pointer')
        self.c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=time_slot)
        self.time = jp.QTime(mask='YYYY-MM-DD HH:mm', format24h=True, name='time', a=self.c2)
        self.time.parent = self
        self.time.value = self.value
        self.time.on('input', self.date_time_change)
        self.append_slot = time_slot

        self.on('change', self.input_change)

        # ------ For debugging the issue --------------
        # count number of changes through the date popup
        self.count_date_changes = jp.QDiv(
                a=self,
                text="0",
                value=0,
                name="count_date_changes"
        )
        # ---------------------------------------------

    @staticmethod
    async def date_time_change(self, msg):
        """
        update all date time values
        """
        # ------ For debugging the issue --------------
        self.parent.count_date_changes.value += 1
        self.parent.count_date_changes.text = self.parent.count_date_changes.value
        # ---------------------------------------------
        print(self.value)
        self.parent.value = self.value  # set input field value
        self.parent.date.value = self.value  # set date selection value
        self.parent.time.value = self.value  # set time selection value

    @staticmethod
    def input_change(self, msg):
        """
        update all date time values
        """
        # ------ For debugging the issue --------------
        self.count_date_changes.value += 1
        self.count_date_changes.text = self.count_date_changes.value
        # ---------------------------------------------
        self.date.value = self.value
        self.time.value = self.value