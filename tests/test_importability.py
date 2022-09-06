"""
Created on 2021-03-20

A basic sanity test

@author: TalAmuyal

"""
from tests.basetest import Basetest  
import io
from contextlib import redirect_stdout
import pprint
    
class TestImportability(Basetest):
    '''
    Tests importability of justpy
    '''
    def test_importability(self):
        '''
        test the import
        '''
        # this actually already runs some code
        with io.StringIO() as outputBuf, redirect_stdout(outputBuf):
            import justpy
            assert justpy
            outputText=outputBuf.getvalue()
        debug=self.debug
        #debug=True
        if debug:
            print(outputText)
        self.assertTrue("Module directory" in outputText)
        self.assertTrue("Application directory" in outputText)
        # https://stackoverflow.com/questions/34861137/list-all-the-elements-in-a-python-namespace
        names=dir(justpy)
        if debug:
            pprint.pprint(names)
            print(f"{len(names)} names found")
        # @TODO - this should be shorter in the future
        self.assertTrue(len(names)>400)    
        pass