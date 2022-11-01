'''
Created on 22.10.2022

@author: wf
'''
from tests.base_client_test import BaseClienttest
import justpy as jp

class TestIssue566(BaseClienttest):
    """
    Tests for websockets
    """
    def test_issue_566_websockets(self):
        
        @jp.app.route("/webpage", name="webpage")
        @jp.app.response
        def hello_world(_request):
            wp = jp.WebPage()
            _d = jp.Div(text='I am justpy webpage', a=wp)
            return wp
  
        jp.WebPage.use_websockets=False
        _response=self.checkResponse("/webpage",debug=False)
        html=_response.text
        print(html)