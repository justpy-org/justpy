"""
Created on 2021-03-20

A basic sanity test

@author: TalAmuyal

"""
from tests.basetest import Basetest  

class TestImportability(Basetest):
    '''
    Tests importability of justpy
    '''
    
    def test_importability(self):
        import justpy
        assert justpy