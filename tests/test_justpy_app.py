"""
Created on 2022-09-14

@author: th
"""
import unittest
from starlette.requests import Request

import justpy as jp
from jpcore.justpy_app import JustpyApp
from jpcore.justpy_config import SESSION_COOKIE_NAME
from tests.base_client_test import BaseClienttest


class TestJustpyApp(BaseClienttest):
    """
    Tests for JustpyApp features
    """

    @unittest.skipIf(BaseClienttest.inPublicCI(), "Setting of cookies currently does not work in the middleware")
    def test_issue_531(self):
        """
        tests error in session handling on invalid session id
        https://github.com/justpy-org/justpy/issues/531
        """
        @jp.app.middleware("http")
        async def add_process_time_header(request: Request, call_next):
            cookies = request.cookies
            cookies[SESSION_COOKIE_NAME] = "invalid token"
            # func = request.app.get_func_for_request(request)
            response = await call_next(request)
            return response

        @jp.app.route("/webpage", name="webpage")
        @jp.app.response
        def hello_world(_request):
            wp = jp.WebPage()
            _d = jp.Div(text='I am justpy webpage', a=wp)
            return wp

        self.app.prioritize_routes()
        _response=self.checkResponse("/webpage",debug=False)
        self.assertIn("Bad Session", _response.text)