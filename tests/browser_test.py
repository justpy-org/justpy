"""
Created on 2022-09-01

@author: wf
"""
from selenium import webdriver
from typing import List
from sys import platform
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumBrowsers:
    """
    handle available selenium drivers/browsers
    """

    def __init__(self, headless: bool = True, cache_valid_range=7):
        self.headless = headless
        self.cache_valid_range = cache_valid_range
        self.browsers = {}

    def getFirst(self):
        """
        get the first available browser
        """
        if len(self.browsers.values()) == 0:
            self.getBrowsers()
        browserList = list(self.browsers.values())
        if len(browserList) > 0:
            return browserList[0]
        else:
            return None

    def getBrowsers(self) -> List[WebDriver]:
        """
        Returns a list of all browsers to test
        """
        if platform == "linux":
            self.browsers["firefox"] = self._getFirefoxWebDriver()
        else:
            self.browsers["chrome"] = self._getChromeWebDriver()
        return self.browsers

    def _getFirefoxWebDriver(self) -> webdriver.Firefox:
        """
        Returns the Firefox selenium webdriver
        """
        options = FirefoxOptions()
        options.headless = self.headless
        browser = webdriver.Firefox(options=options)
        return browser

    def _getChromeWebDriver(self) -> webdriver.Chrome:
        """
        Returns the Chrome selenium webdriver
        """
        options = ChromeOptions()
        options.headless = self.headless
        chrome_executable = ChromeDriverManager(cache_valid_range=365).install()
        service = ChromeService(chrome_executable)
        browser = webdriver.Chrome(service=service, options=options)
        return browser
