"""
Created on 2022-09-05

@author: wf
"""
from tests.base_server_test import BaseAsynctest
from tests.basetest import Basetest
from jpcore.demostarter import Demostarter
import unittest
import asyncio

class TestDemoStarter(BaseAsynctest):
    """
    test demo starter
    """

    async def setUp(self):
        await BaseAsynctest.setUp(self, with_server=False)

    @unittest.skipIf(Basetest.inPublicCI(), "demostarter ")
    async def testDemoStarter(self):
        """
        test the demo starter
        """
        demoStarter = Demostarter(debug=True, mode="process")

        await demoStarter.start(limit=2)

        # wait a bit
        await asyncio.sleep(2.0)
        # stop all servers
        await demoStarter.stop()
        with self.subTest("testDemoStarter", demoStarter=demoStarter):
            self.assertEqual(0, len(demoStarter.errors.values()))
