'''
Created on 2022-08-30

@author: @sandeep-gh
@author: wf

see https://github.com/justpy-org/justpy/issues/478 
and https://github.com/justpy-org/justpy/issues/389
'''
import justpy as jp
from starlette.testclient import TestClient
from tests.basetest import Basetest

@jp.SetRoute("/bye", name = "bye")
def bye_function(_request):
    wp = jp.WebPage()
    wp.add(jp.P(text='Hello there!', classes='text-5xl m-2'))
    return wp

@jp.SetRoute("/hello", name = "hello")
def hello_function(request):
    wp = jp.WebPage()
    wp.add(jp.P(text='Hello there!', classes='text-5xl m-2'))
    print("request  = ", request.url_for("bye"))
    return wp

class TestUrlFor(Basetest):
    '''
    test the url_for functionality
    '''
    
    def testUrlFor(self):
        app = jp.app
        client = TestClient(app)
        if not self.inPublicCI():
            client.get("/hello")    