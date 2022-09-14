'''
Created on 2022-09-13

@author: wf
'''
import justpy as jp
from tests.basetest import Basetest
from starlette.testclient import TestClient

class BaseClienttest(Basetest):
    """
    Basetests using the starlette TestClient
    """
    
    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.app = jp.app
    
    def checkResponse(self, path, expected_code=200, debug: bool = None):
        """
        check the response for the given path

        Args:
            path(str): the path to check
            expected_code(int): the HTTP status code to expect
            debug(bool): if True show debugging info
        """
        if debug is None:
            debug = self.debug
        if debug:
            print(f"checking response for {path}")
        with TestClient(self.app) as client:
            response = client.get(path)
            self.assertEqual(expected_code, response.status_code)
        if debug:
            print(response.text)
        return response
