"""
Created on 2022-09-01

@author: wf
"""
import aiohttp
import asynctest
from jpcore.justpy_app import JustpyServer
from tests.basetest import Basetest, Profiler


class BaseAsynctest(asynctest.TestCase):
    """
    basic asynch test
    """

    # https://github.com/encode/starlette/blob/master/docs/testclient.md

    async def setUp(
        self,
        port: int = 8123,
        host: str = "127.0.0.1",
        sleep_time=None,
        with_server=True,
        debug=False,
        profile=True,
        mode=None,
    ):
        """Bring server up.

        Args:
            wpfunc: the (async) function for the webpage
            port(int): the port
            host(str): the host
            sleep_time(float): the time to sleep after server process was started
            debug(bool): if True debugging is on
            profile(bool): if True time for test is profiled
        """
        if sleep_time is None:
            sleep_time = 2.0 if Basetest.inPublicCI() else 0.75
        self.sleep_time = sleep_time
        self.server = None
        if with_server:
            self.server = JustpyServer(
                port=port, host=host, sleep_time=sleep_time, mode=mode, debug=debug
            )
        self.debug = debug
        self.profile = profile
        msg = f"test {self._testMethodName}, debug={self.debug}"
        self.profiler = Profiler(msg, profile=self.profile)

    async def tearDown(self):
        """Shutdown the app."""
        if self.server is not None:
            await self.server.stop()
        self.profiler.time()

    def getUrl(self, path):
        """
        get the url for the given path

        Args:
            path(str): the path
        Returns:
            str: the url for the path

        """
        url = f"http://{self.server.host}:{self.server.port}{path}"
        return url

    async def getResponseHtml(self, path: str = "/"):
        """
        get the status and raw html for the given path

        Args:
            path(str): the path
        Returns:
            status,rawhtml
        """
        async with aiohttp.ClientSession() as session:
            url = self.getUrl(path)
            async with session.get(url) as resp:
                rawhtml = await resp.content.read()
                status = resp.status
        return status, rawhtml
