"""
Created on 2022-09-18

@author: th
"""
import asyncio
import unittest
import pandas as pd
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import justpy as jp
from tests.base_selenium_test import BaseSeleniumTest
from selenium.webdriver.support import expected_conditions as EC

class TestIssue304(BaseSeleniumTest):
    """
    testing issue 304
    https://github.com/justpy-org/justpy/issues/304
    """

    async def tearDown(self):
        """
        close selenium browser and stop server
        """
        self.browser.close()
        await self.server.stop()

    async def test_issue_30(self):
        """
        test when the issue occurs that input and input display differ
        """
        await self.server.start(self.issue_page)
        url = self.server.get_url("/")
        self.browser.get(url)
        timeout = 5
        driver = self.get_waiting_browser(self.browser)
        # wait until a row is clickable
        self.assertTrue(
                driver.until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "ag-cell"))
                ),
                "After loading the page an ag-cell should be clickable"
        )
        # click cells since the row div does not register a click
        cells = self.browser.find_elements(By.CLASS_NAME, "ag-cell")
        cells[18*2].click()
        # test row single click
        self.assertTrue(
                driver.until(
                        EC.text_to_be_present_in_element(
                                locator=(By.NAME, "test_row_clicked"),
                                text_="Clicked")
                )
        )
        # test row double click
        action_chains = ActionChains(self.browser)
        action_chains.double_click(cells[18*3]).perform()
        self.assertTrue(
                driver.until(
                        EC.text_to_be_present_in_element(
                                locator=(By.NAME, "test_row_double_clicked"),
                                text_="Clicked")
                )
        )

    @unittest.skipIf(True, "Only for manual testing")
    def test_manual(self):
        """
        start the server to test the issue manually
        """
        jp.justpy(self.issue_page, port=8500)

    @staticmethod
    def get_sample_data() -> pd.DataFrame:
        """
        returns a dataframe with sample data
        """
        wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
        return wm_df

    @staticmethod
    def row_clicked(self, msg):
        """
        row select event handler
        """
        # print("row clicked (single)")
        if msg.selected:
            self.row_data_div.text = msg.data
            self.row_selected = msg.rowIndex
            self.a.test_row_clicked.text = "Clicked"
        elif self.row_selected == msg.rowIndex:
            self.row_data_div.text = ''

    @staticmethod
    def row_double_clicked(self, msg):
        """
        row select event handler
        """
        # print("row double-clicked")
        if msg.selected:
            self.row_data_div.text = msg.data
            self.row_selected = msg.rowIndex
            self.a.test_row_double_clicked.text = "Clicked"
        elif self.row_selected == msg.rowIndex:
            self.row_data_div.text = ''

    @staticmethod
    def issue_page():
        """
        page containing the issue
        """
        wp = jp.WebPage()
        row_data_div = jp.Div(a=wp)
        grid = TestIssue304.get_sample_data().jp.ag_grid(a=wp)
        grid.row_data_div = row_data_div
        grid.on('rowClicked', TestIssue304.row_clicked)
        grid.on('rowDoubleClicked', TestIssue304.row_double_clicked)
        grid.options.columnDefs[0].checkboxSelection = True
        grid.options.rowSelection = 'single'
        wp.test_row_clicked = jp.Div(a=wp, name="test_row_clicked")
        wp.test_row_double_clicked = jp.Div(a=wp, name="test_row_double_clicked")
        return wp
