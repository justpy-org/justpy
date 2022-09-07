"""
Created on 2022-09-07

@author: hr
"""
import hjson

from tests.basetest import Basetest
from addict import Dict


class TestJavaScriptObject(Basetest):
    """
    Tests JavaScript object conversion via PyYaml
    """

    def test_decode(self):
        """
        test JavaScript object decoding
        """
        # example options string see
        # https://www.highcharts.com/docs/getting-started/how-to-set-options
        options_string = """{
    chart: {
        renderTo: 'container',
        type: 'bar'
    },
    title: {
        text: 'Fruit Consumption'
    },
    xAxis: {
        categories: ['Apples', 'Bananas', 'Oranges']
    },
    yAxis: {
        title: {
            text: 'Fruit eaten'
        }
    },
    series: [{
        name: 'Jane',
        data: [1, 0, 4]
    }, {
        name: 'John',
        data: [5, 7, 3]
    }]
}"""
        options = Dict(hjson.loads(options_string.encode("ascii", "ignore")))
        debug = self.debug
        # debug=True
        if debug:
            print(options)
        self.assertTrue("chart" in options)
        pass

    def test_decode_no_separating_spaces(self):
        """
        test JavaScript object decoding
        """
        # example options string see
        # https://www.highcharts.com/docs/getting-started/how-to-set-options
        options_string = """{
    title:{
        text:'Fruit Consumption'
    },
    xAxis: {
        categories: ['Apples', 'Bananas', 'Oranges']
    },
    series:[]
}"""
        options = Dict(hjson.loads(options_string.encode("ascii", "ignore")))
        debug = self.debug
        # debug=True
        if debug:
            print(options)
        self.assertTrue("series" in options)
        self.assertTrue("title" in options)
        self.assertTrue("text" in options["title"])

    def test_decode_dirty_js(self):
        """
        test decoding of dirty JavaScript objects
        """
        dirty_js = """
             {
          key: "value",
          "key2":"value"
        }
        """
        options = hjson.loads(dirty_js)
        self.assertTrue("key2" in options)
        self.assertTrue("key" in options)

    def test_decode_dirty_js2(self):
        """
        test decoding of dirty JavaScript objects
        cf. https://stackoverflow.com/questions/34812821/bad-json-keys-are-not-quoted
        """
        dirty_js = """
             {
          key:"value",
          "key2":"value"
        }
        """
        options = hjson.loads(dirty_js)
        self.assertTrue("key2" in options)
        self.assertTrue("key" in options)
