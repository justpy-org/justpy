"""
Created on 2022-08-26

@author: wf
"""
from tests.basetest import Basetest
from justpy.quasarcomponents import QInput


class TestQuasar(Basetest):
    """
    test Quasar components

    https://quasar.dev/vue-components
    """

    def testQInput(self):
        """
        test QInput
        """
        qInput = QInput()
        propList = qInput.prop_list
        debug = True
        if debug:
            print(propList)
        self.assertTrue("loading" in propList)
