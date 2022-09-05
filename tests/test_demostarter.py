'''
Created on 2022-09-05

@author: wf
'''
from tests.base_server_test import BaseAsynctest
from jpcore.demostarter import Demostarter
import asyncio

class TestDemoStarter(BaseAsynctest):
    '''
    test demo starter
    '''
    
    async def setUp(self):
        await BaseAsynctest.setUp(self,with_server=False)
    
    async def testDemoStarter(self):
        '''
        test the demo starter
        '''
        demoStarter=Demostarter(debug=True)
        await demoStarter.start(limit=None)
        self.assertEqual(0,len(demoStarter.errors.values()))
        # wait a bit 
        await asyncio.sleep(2.0)
        # stop all servers
        await demoStarter.stop()
        pass
    