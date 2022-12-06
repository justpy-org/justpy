"""
Created on 2022-09-17

@author: th
"""
from tests.basetest import Basetest
from justpy.gridcomponents import AgGrid

class TestIssue620(Basetest):
    """
    testing issue 620
    https://github.com/justpy-org/justpy/issues/620
    """

    def test_issue_620(self):
        """
        test a lod loading
        """
        lod=[
            {
                "family_name":"Doe",
                "given_name":"John",
            }
        ]
        ag_grid=AgGrid()
        ag_grid.load_lod(lod)
        if self.debug:
            print(ag_grid.options.columnDefs)
        expected=[{'field': 'family_name', 'filter': True}, {'field': 'given_name', 'filter': True}]
        self.assertEqual(expected, ag_grid.options.columnDefs)
        