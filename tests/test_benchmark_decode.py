"""
Created on 2022-09-05

@author: hr
"""
from timeit import timeit

import yaml
import hjson
import demjson3 as demjson

from tests.basetest import Basetest


class TestBenchmarkDecode(Basetest):
    """
    Benchmarks decoding performance
    """

    # example options string see
    # https://www.highcharts.com/docs/getting-started/how-to-set-options
    options_string: str = """{
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

    def test_decode_time_demjson(self):
        """
        test demjson
        """
        elapsed = timeit(lambda: demjson.decode(self.options_string.encode("ascii", "ignore")), number=1000)
        print(f'Time: {elapsed:.2f}s')
        self.assertGreater(elapsed, 0.0)

    def test_decode_time_yaml(self):
        """
        test yaml
        """

        elapsed = timeit(lambda: yaml.full_load(self.options_string.encode("ascii", "ignore")),
                         number=1000)
        print(f'Time: {elapsed:.2f}s')
        self.assertGreater(elapsed, 0.0)

    def test_decode_time_hjson(self):
        """
        test hjson
        """

        elapsed = timeit(lambda: hjson.loads(self.options_string.encode("ascii", "ignore")),
                         number=1000)
        print(f'Time: {elapsed:.2f}s')
        self.assertGreater(elapsed, 0.0)
