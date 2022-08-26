'''
Created on 2022-08-24

@author: wf
'''
import justpy as jp
from tests.basetest import BaseAsynctest

class TestJustpyCore(BaseAsynctest):
    '''
    Tests for Justpy Core features
    '''
    async def setUp(self):
        await BaseAsynctest.setUp(self, self.wp_to_test)
        
    async def wp_to_test(self):
        '''
        the example Webpage under test
        '''
        wp = jp.WebPage()
        _d=jp.Div(a=wp)
        return wp
        
    
    async def testWp(self):
        ''''
        test the webpage asynchronously
        '''
        status,rawhtml=await self.getResponseHtml()
        self.assertEqual(200,status)        
        html=rawhtml.decode("utf8")
        debug=True
        if debug:
            print(html)

    
    

