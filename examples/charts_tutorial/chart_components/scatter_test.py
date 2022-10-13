# Justpy Tutorial demo scatter_test from docs/charts_tutorial/chart_components.md
import justpy as jp
import numpy as np

class ScatterWithRegression(jp.Scatter):

    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, **kwargs)
        x = np.asarray(x)
        y = np.asarray(y)
        m = (len(x) * np.sum(x * y) - np.sum(x) * np.sum(y)) / (len(x) * np.sum(x * x) - np.sum(x) ** 2)
        b = (np.sum(y) - m * np.sum(x)) / len(x)
        s = jp.Dict()   # The new series
        s.type = 'line'
        s.marker.enabled = False
        s.enableMouseTracking = False
        min = float(x.min())
        max = float(x.max())
        s.data = [[min, m * min + b], [max, m * max + b]]
        s.name = f'Regression, m: {round(m, 3)}, b: {round(b, 3)}'
        self.options.series.append(s)


def scatter_test(request):
    wp = jp.WebPage(highcharts_theme='grid-light')
    x = [108,19,13,124,40,57,23,14,45,10,5,48,11,23,7,2,24,6,3,23,6,9,9,3,29,7,4,20,7,4,0,25,6,5,22,11,61,12,4,16,13,60,41,37,55,41,11,27,8,3,17,13,13,15,8,29,30,24,9,31,14,53,26]
    y = [392.5,46.2,15.7,422.2,119.4,170.9,56.9,77.5,214,65.3,20.9,248.1,23.5,39.6,48.8,6.6,134.9,50.9,4.4,113,14.8,48.7,52.1,13.2,103.9,77.5,11.8,98.1,27.9,38.1,0,69.2,14.6,40.3,161.5,57.2,217.6,58.1,12.6,59.6,89.9,202.4,181.3,152.8,162.8,73.4,21.3,92.6,76.1,39.9,142.1,93,31.9,32.1,55.6,133.3,194.5,137.9,87.4,209.8,95.5,244.6,187.5]
    jp.Scatter(x, y, a=wp, classes='m-2 w-1/2 border', style='height: 300px')
    sr = ScatterWithRegression(x, y, a=wp, classes='m-2 w-1/2 border', style='height: 300px')
    sr.options.title.text = 'Scatter Chart with Regression'
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("scatter_test",scatter_test)
