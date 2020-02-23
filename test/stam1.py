import justpy as jp
import numpy as np


def sine_test():
    wp = jp.WebPage()
    chart = jp.HighCharts(a=wp, classes='border m-2 p-2 w-3/4')
    chart.options.title.text = 'Sines Galore'  # https://api.highcharts.com/highcharts/title.text
    x = np.linspace(-np.pi, np.pi, 201)
    for frequency in range(1,11):
        y = np.sin(frequency * x)
        chart.options.series.append({'name': f'F{frequency}', 'data': list(zip(x, y))})
    return wp


jp.justpy(sine_test)
