'''
Created on 2022-08-24

@author: wf
'''
# https://github.com/encode/starlette/blob/master/docs/testclient.md
# https://stackoverflow.com/questions/57412825/how-to-start-a-uvicorn-fastapi-in-background-when-testing-with-pytest

from multiprocessing import Process
import justpy as jp
import asynctest
import aiohttp
import asyncio

class TestJustpyCore(asynctest.TestCase):
    '''
    Tests for Justpy Core features
    '''
    async def wp_to_test(self):
        '''
        the example Webpage under test
        '''
        wp = jp.WebPage()
        _d=jp.Div(a=wp)
        return wp
    
    async def setUp(self):
        """ Bring server up. """
        self.port=8123
        self.proc = Process(target=jp.justpy,
                            args=(self.wp_to_test,),
                            kwargs={
                                "host": "127.0.0.1",
                                "port": self.port,
                            },
                            daemon=True)
        self.proc.start()
        await asyncio.sleep(0.5)  # time for the server to start
        
    async def tearDown(self):
        """ Shutdown the app. """
        self.proc.terminate()
        
    
    async def testWp(self):
        ''''
        test the webpage asynchronously
        '''
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://127.0.0.1:{self.port}/") as resp:
                rawhtml = await resp.content.read()
                status = resp.status
        self.assertEqual(200,status)        
        html=rawhtml.decode("utf8")
        debug=True
        if debug:
            print(html)

    
    

