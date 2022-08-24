'''
Created on 2022-08-20

@author: wf
'''
from tests.basetest import Basetest  
import demjson3 as demjson
from addict import Dict

class TestDemJson(Basetest):
    '''
    Tests demjson
    '''

    def testDemjson(self):
        '''
        test demjson
        '''
        # example options string see
        # https://www.highcharts.com/docs/getting-started/how-to-set-options
        options_string="""{
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
        options = Dict(demjson.decode(options_string.encode("ascii", "ignore")))
        debug=self.debug
        #debug=True
        if debug:
            print(options)
        self.assertTrue("chart" in options)
        pass