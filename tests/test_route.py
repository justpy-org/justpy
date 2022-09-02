'''
Created on 2022-08-30

@author: @sandeep-gh
@author: wf

see https://github.com/justpy-org/justpy/issues/478 
and https://github.com/justpy-org/justpy/issues/389
'''
import justpy as jp
from starlette.testclient import TestClient
from justpy.routing import JpRoute
from tests.basetest import Basetest

@jp.SetRoute("/bye", name = "bye")
def bye_function(_request):
    wp = jp.WebPage()
    wp.add(jp.P(text='Bye bye!', classes='text-5xl m-2'))
    return wp

@jp.SetRoute("/hello", name = "hello")
def hello_function(request):
    wp = jp.WebPage()
    wp.add(jp.P(text='Hello there!', classes='text-5xl m-2'))
    #print("request  = ", request.url_for("hello"))
    return wp

class TestRouteAndUrlFor(Basetest):
    '''
    test the url_for functionality
    '''
    
    def testRoute(self):
        '''
        test the routing
        '''
        self.assertEqual(2,len(JpRoute.routesByPath))
        debug=self.debug
        #debug=True
        for route in JpRoute.routesByPath.values():
            routeAsText=str(route)
            if debug:
                print(routeAsText)
        for path in ["/bye","/hello"]:
            self.assertTrue(path in JpRoute.routesByPath)
       
    def testUrlFor(self):
        '''
        test url for functionality
        '''
        app = jp.app
        # see https://www.starlette.io/testclient/
        with TestClient(app) as client:
            response=client.get("/hello")    
            self.assertEqual(200,response.status_code)
            debug=self.debug
            debug=True
            lines=response.text.split("\n")
            if debug:
                print(response.text)
                print(f"{len(lines)} lines")
            self.assertTrue(response.text.startswith("<!DOCTYPE html>"))
            self.assertTrue(len(lines)<500)