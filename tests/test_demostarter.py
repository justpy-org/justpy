"""
Created on 2022-09-05

@author: wf
"""
from tests.base_server_test import BaseAsynctest
from tests.basetest import Basetest
from jpcore.demostarter import Demostarter
import unittest
import asyncio
import pprint

class TestDemoStarter(BaseAsynctest):
    """
    test demo starter
    """

    async def setUp(self):
        await BaseAsynctest.setUp(self, with_server=False)
        
    def testVideos(self):
        """
        test video availability
        """
        demoStarter = Demostarter(debug=True, mode="process")
        lod=demoStarter.as_list_of_dicts()
        debug=True
        if debug:
            pprint.pprint(lod)
        foundVideos=0
        for record in lod:
            video=record.get("video")
            if video:
                foundVideos+=1
        if debug:
            print(f"found {foundVideos} videos")
        self.assertTrue(foundVideos>=3)

    @unittest.skipIf(Basetest.inPublicCI(), "demostarter ")
    async def testDemoStarter(self):
        """
        test the demo starter
        """
        #@TODO reenable test
        return 
        demoStarter = Demostarter(debug=True, mode="process")

        await demoStarter.start(limit=2)

        # wait a bit
        await asyncio.sleep(2.0)
        # stop all servers
        await demoStarter.stop()
        with self.subTest("testDemoStarter", demoStarter=demoStarter):
            self.assertEqual(0, len(demoStarter.errors.values()))
