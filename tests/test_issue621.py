"""
Created on 2022-11-15

@author: th
"""
from tests.basetest import Basetest
from jpcore.compat import Compatibility

class TestIssue621(Basetest):
    """
    testing issue 621
    https://github.com/justpy-org/justpy/issues/621
    """

    def test_issue_621(self):
        """
        test singleton behavior
        """
        from jpcore.justpy_config import JpConfig
        JpConfig.reset()
        Compatibility(0,11,1)
        self.assertIsNone(JpConfig.config)
        JpConfig.config=JpConfig()
        Compatibility.reset()
        