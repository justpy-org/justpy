"""
Created on 2022-11-14

@author: th
"""
import asyncio
import datetime

import pandas as pd


import justpy as jp
from tests.base_selenium_test import BaseSeleniumTest


class TestAgGrid(BaseSeleniumTest):
    """
    testing AgGrid integration
    """

    async def setUp(self, **kwargs):
        """
        setup test environment
        """
        await super().setUp(port=8124, **kwargs)
        self.data = [
            {"name": "Bob", "age": 42, "birthdate": datetime.date(year=2000, month=1, day=1)},
            {"name": "Alice", "age": 24, "birthdate": datetime.date(year=2022, month=1, day=1)},
        ]

    async def tearDown(self):
        """
        close test environment
        """
        self.browser.close()
        await asyncio.sleep(self.server.sleep_time)
        await self.server.stop()

    async def test_load_pandas_frame(self):
        """
        tests loading a pandas dataframe into AgGrid
        """

        def table_from_dataframe() -> jp.WebPage:
            """
            load AgGrid from dataframe
            """
            df = pd.DataFrame.from_records(self.data)
            df['birthdate'] = pd.to_datetime(df['birthdate'])
            wp = jp.WebPage()
            aggrid_table = jp.AgGrid(a=wp)
            aggrid_table.load_pandas_frame(df)
            return wp

        await self.server.start(table_from_dataframe)
        url = self.server.get_url("/")
        # test setting of col_filter

        # test display of data
