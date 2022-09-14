"""
Created on 2022-08-30

@author: @sandeep-gh
@author: wf

see https://github.com/justpy-org/justpy/issues/478 
and https://github.com/justpy-org/justpy/issues/389
"""
from tests.base_client_test import BaseClienttest
import justpy as jp
from starlette.responses import PlainTextResponse
from jpcore.justpy_config import HTML_404_PAGE

@jp.app.route("/plaintext")
async def plainText(_request):
    return PlainTextResponse("Plaintext")

@jp.app.route("/urlFor/{name}")
async def urlFor(request):
    name=request.path_params["name"]
    print(f"calling url_for {name}")
    url=request.url_for(name)
    return PlainTextResponse(url)

@jp.app.route("/greet/{name}")
@jp.app.response
def greeting_function(request):
    wp = jp.WebPage()
    name = f"""{request.path_params["name"]}"""
    wp.add(jp.P(text=f"Hello there, {name}!", classes="text-5xl m-2"))
    return wp

@jp.app.jproute("/bye")
def bye_function(_request):
    wp = jp.WebPage()
    wp.add(jp.P(text="Bye bye!", classes="text-5xl m-2"))
    return wp

@jp.app.route("/hello",name="hello")
@jp.app.response
def hello_function(_request):
    wp = jp.WebPage()
    wp.add(jp.P(text="Hello there!", classes="text-5xl m-2"))
    # print("request  = ", request.url_for("hello"))
    return wp

class TestRouteAndUrlFor(BaseClienttest):
    """
    test the url_for functionality
    """

    def setUp(self, debug=False, profile=True):
        BaseClienttest.setUp(self, debug=debug, profile=profile)
        self.app.prioritize_routes()
        
    def testStarletteRoutes(self):
        """
        test the starlette Routes
        """
        debug=True
        for i,route in enumerate(self.app.router.routes):
            route_as_text = self.app.route_as_text(route)
            if debug:
                print(f"{i}:{route_as_text}")
            

    def testJpRoute(self):
        """
        Test the routing
        """
        routes=self.app.router.routes
        self.assertTrue(len(routes)>=9)
        debug = self.debug
        debug=True
        for path in ["/bye", "/hello", "/greet/{name}"]:
            found=False
            for route in routes:
                found=route.path==path
                if found:
                    break
            self.assertTrue(found)

    def testUrlFor(self):
        """
        Test url for functionality
        """
        for name,url in [
            ("plainText","plaintext"),
            ("hello","hello"),
            ("bye_function","bye")
        ]:
            path=f"/urlFor/{name}"
            response=self.checkResponse(path)
            urlfor=response.text
            print(urlfor)
            self.assertEqual(urlfor,f"http://testserver/{url}")
            pass
    
    def testResponses(self):
        
        for path in [
            "/plaintext",
            #"/hello","/greet/eli","/bye"
            ]:
            _response=self.checkResponse(path,debug=True)

    def testInvalidPath(self):
        """
        test handling an invalid path
        """
        response = self.checkResponse("/invalidpath", 404)
        #self.assertEqual(HTML_404_PAGE, response.text)

    def testStaticPath(self):
        """
        test handling static content
        """
        response = self.checkResponse("/templates/js/justpy_core.js")
        self.assertTrue("class JustpyCore" in response.text)
        response = self.checkResponse("/templates/css/invalid_css.css", 404)

    def testHtmlContent(self):
        # see https://www.starlette.io/testclient/
        response = self.checkResponse("/hello")
        debug = self.debug
        debug = True
        lines = response.text.split("\n")
        if debug:
            print(response.text)
            print(f"{len(lines)} lines")
        self.assertTrue(response.text.startswith("<!DOCTYPE html>"))
        self.assertTrue(len(lines) < 80)
