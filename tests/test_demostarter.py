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
        
    def test_videos(self):
        """
        test video availability
        """
        demo_starter = Demostarter(debug=True, mode="process")
        debug=True
        foundVideos=0
        for demo in demo_starter.demos:
            if demo.video_url is not None:
                foundVideos+=1
        if debug:
            print(f"found {foundVideos} videos")
        self.assertTrue(foundVideos>=30)
        
    def test_example_sources(self):
        """
        test example source handling
        """
        demo_starter = Demostarter()
        debug=self.debug
        debug=True
        for demo in demo_starter.demos:
            if debug:
                print(demo)

    @unittest.skipIf(Basetest.inPublicCI(), "demostarter ")
    async def test_demo_starter(self):
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
