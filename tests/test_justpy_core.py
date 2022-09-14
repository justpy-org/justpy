"""
Created on 2022-08-24

@author: wf
"""
import justpy as jp
from tests.base_server_test import BaseAsynctest

class TestJustpyCore(BaseAsynctest):
    """
    Tests for Justpy Core features
    """

    async def setUp(self):
        await BaseAsynctest.setUp(self, port=8122, debug=True)

    async def wp_to_test(self):
        """
        the example Webpage under test
        """
        wp = jp.WebPage()
        _d = jp.Div(a=wp)
        return wp

    async def testWp(self):
        """'
        test the webpage asynchronously
        """
        await self.server.start(self.wp_to_test)
        status, rawhtml = await self.getResponseHtml()
        self.assertEqual(200, status)
        html = rawhtml.decode("utf8")
        debug = True
        if debug:
            print(html)
            with open("/tmp/justpy.html", "w") as html_file:
                print(html, file=html_file)
