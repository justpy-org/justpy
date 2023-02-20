import typing
import unittest
import urllib.request
from unittest import IsolatedAsyncioTestCase

import requests
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, Response

from jpcore.justpy_app import JustpyServer
import justpy as jp
from uuid import uuid4

from tests.basetest import Basetest


@unittest.skipIf(Basetest.inPublicCI(), "")
class TestRestful(IsolatedAsyncioTestCase):
    """
    tests justpy restful capabilities
    """

    async def asyncSetUp(self):
        """
        setup restful server
        """
        await super().asyncSetUp()
        self.server = RESTfulServer()
        await self.server.start(self.server.get_homepage)

    async def asyncTearDown(self):
        """
        tear down the restful server
        """
        await self.server.stop()
        super(TestRestful, self).tearDown()


    def test_json_response(self):
        """
        test json response of the restful server with GET request
        """
        res = requests.get(self.server.get_url("/json"))
        expected = {'hello': 'world'}
        self.assertDictEqual(expected, res.json())

    def test_json_post_response(self):
        """
        test json response of the restful server with POST request
        """
        expected = {'hello': 'world', "method": 'POST'}
        res = requests.post(self.server.get_url("/json_post"),data=expected)
        self.assertDictEqual(expected, res.json())

    @unittest.skip
    def test(self):
        """
        test Restful server manually
        """
        while True:
            pass


class RESTfulServer(JustpyServer):
    """
    justpy RESTful server to test RESTful routes and redirects
    """

    def __init__(self, **kwargs):
        """
        constructor
        """
        super(RESTfulServer, self).__init__(**kwargs)
        jp.Route("/hello/{name}", self.hello_webpage)
        jp.Route("/json", self.json_route)
        jp.Route("/json_post", self.json_post_route, methods=["POST"])

    def get_homepage(self) -> jp.WebPage:
        """
        Get the homepage/root page of the server
        """
        wp = jp.WebPage()
        div = jp.Div(a=wp, classes="container mx-auto", text="justpy RESTful api Test")
        buttons_div = jp.Div(a=div, classes="flex flex-col gap-4")
        jp.Button(a=buttons_div, classes="bg-blue-500", on_click=self.redirect_to_hellopage, text="Test Redirect")
        jp.Button(a=buttons_div, classes="bg-blue-500", on_click=self.redirect_with_post, text="Test Redirect with POST")
        return wp

    def redirect_to_hellopage(self, msg):
        """
        handle Test redirect button click by redirecting to different justpy route
        """
        wp: jp.WebPage = msg.get("page")
        wp.redirect = self.get_url("/hello/Test")

    async def redirect_with_post(self, msg):
        """
        Redirect with a POST request that contains data
        """
        wp: jp.WebPage = msg.get("page")
        target_url = "/json_post"
        data = {"name": "Homer", "age": 42}
        await JustpyWindowByPOST.send_post_request(data=data, wp=wp, target_url=target_url)

    def hello_webpage(self, req: Request) -> jp.WebPage:
        """
        Get the Hello Webpage that greets the name wntered in the url path
        e.g. /hello/Joe  → "Hello Joe"
        Args:
            req: page request containing the url parameter
        """
        name = req.path_params.get("name", None)
        webpage = jp.WebPage()
        jp.Div(a=webpage, text=f" Hello {name}", classes="container")
        return webpage

    def json_route(self, req: Request) -> JSONResponse:
        """
        returns json

        Args:
            req: request

        Returns:
            JSONResponse
        """
        return JSONResponse({'hello': 'world'})

    async def json_post_route(self, req: Request) -> JSONResponse:
        """
        Expects a POST request with either the data being in JSON or forms format
        Retruns the data as json
        Args:
            req: request

        Returns:
            JSONResponse
        """
        try:
            data = await req.json()
        except Exception as ex:
            try:
                form_data = await req.form()
                data = {k: v for k, v in form_data.items()}
            except Exception as ex:
                data = {
                    "error": "Data could not be extracted from the request",
                    "msg": ex
                }
                print(ex)
        print(data)
        return JSONResponse(data)


class JustpyWindowByPOST:
    """
    Provides functionality to open a new window/tab by POST request with data
    """

    @classmethod
    async def send_post_request(cls, data: dict, wp: jp.WebPage, target_url: str, target: typing.Optional[str] = None):
        """
        Args:
            data: data to send in the POST request
            wp: webpage
            target_url: URL to send the POST request to
            target: where to display the response. Default: _blank see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form#attr-target
        """
        if target is None:
            target = "_blank"
        uuid = str(uuid4())
        data_inputs = []
        for key, value in data.items():
            input_field = f"""<input id="{uuid}_{key}" name="{key}" type="hidden" value="{value}">"""
            data_inputs.append(input_field)
        js = f"""
        console.log("Sending Post Request");
        let html = `
        <form id="{uuid}_form" action="{target_url}" method="post" target="{target}">
            {'<br>'.join(data_inputs)}
        </form>`;
        console.log(html);
        let inv_form = document.createElement('div');
        inv_form.setAttribute("type", "hidden");
        inv_form.innerHTML = html.trim();
        document.body.appendChild(inv_form);
        let form = document.getElementById("{uuid}_form");
        console.log(new FormData(form));
        form.submit(); 
        inv_form.remove()
        """
        print("Executing", js)
        await wp.run_javascript(js)

