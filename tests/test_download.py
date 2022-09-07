"""
Created on 29.08.2022

@author: wf
"""
from tests.basetest import Basetest
from jpcore.download import Download
import os


class TestDownlad(Basetest):
    """
    test the download utility class
    """

    def testDownloadChinookDb(self):
        """
        see https://justpy.io/grids_tutorial/database/
        """
        dbname = "chinook.db"
        url = f"https://elimintz.github.io/{dbname}"
        os.makedirs(Download.get_cache_path(), exist_ok=True)
        filePath = f"{Download.get_cache_path()}/{dbname}"
        Download.download_file(url, dbname, target_directory=Download.get_cache_path())
        self.assertTrue(os.path.isfile(filePath))
