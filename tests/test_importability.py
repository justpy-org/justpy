"""
Created on 2021-03-20

A basic sanity test

@author: TalAmuyal

"""
from tests.basetest import Basetest  
import io
from contextlib import redirect_stdout
    
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
            debug=self.debug
            #debug=True
            outputText=outputBuf.getvalue()
        if debug:
            print(outputText)
        self.assertTrue("Module directory" in outputText)
        self.assertTrue("Application directory" in outputText)