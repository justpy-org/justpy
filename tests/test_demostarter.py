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
    
    async def testDemoStarter(self):
        '''
        test the demo starter
        '''
        demoStarter=Demostarter(debug=True)
        await demoStarter.start(limit=None)
        
        await asyncio.sleep(5.0)
        await demoStarter.stop()
        pass
    