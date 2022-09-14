"""
Created on 2022-09-13

@author: wf
"""
import justpy as jp
from starlette.requests import Request
from tests.base_client_test import BaseClienttest
import time
# https://fastapi.tiangolo.com/tutorial/middleware/
@jp.app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    func=request.app.get_func_for_request(request)
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@jp.app.route("/webpage", name="webpage")
@jp.app.response
def hello_world(_request):
    wp = jp.WebPage()
    _d = jp.Div(text='I am justpy webpage',a=wp)
    return wp

class TestMiddleWare(BaseClienttest):
    """
    test FASTAPI middleware 
    """
    
    def setUp(self, debug=False, profile=True):
        BaseClienttest.setUp(self, debug=debug, profile=profile)
        self.app.prioritize_routes()
    
    def test_middleware(self):
        """
        test the middleware 
        """
        _response=self.checkResponse("/webpage",debug=False)
        pass
        