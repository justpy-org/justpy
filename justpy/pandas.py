
from .chartcomponents import *
import pandas as pd
import itertools

_high_charts_colors = ["#7cb5ec", "#434348", "#90ed7d", "#f7a35c", "#8085e9", "#f15c80", "#e4d354", "#2b908f", "#f45b5b", "#91e8e1"]

_s1 = """
{
    chart: {
        type: 'spline',
        zoomType: 'xy'
    },

    title: {
        text: 'Pandas Chart Title'
    },

    subtitle: {
        text: 'Pandas Chart Subtitile'
    },

    yAxis: {
        title: {
            text: 'Y Axis Title'
        }
    },

    xAxis: {
        title: {
            text: 'X Axis Title'
        }
    },

    legend: {
        layout: 'proximate',
        align: 'right'

    },


    series: [],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

}

"""


def make_pairs_list(x_data, y_data):
    return list(map(list, itertools.zip_longest(x_data, y_data)))

def get_index_data(df, chart=None):
    if isinstance(df.index, pd.DatetimeIndex):
        x_data = [x.value // 1000000 for x in df.index.to_list()]
        # https://api.highcharts.com/highcharts/xAxis.type
        if chart:
            chart.options.xAxis.type = 'datetime'
    elif isinstance(df.index, pd.Int64Index) or isinstance(df.index, pd.Float64Index):
        x_data = df.index.to_list()
    else:
        raise TypeError('Dataframe Index type not number or datetime')
    return x_data

def set_chart_kwargs(chart, kwargs):
    if 'width' in kwargs:
        chart.options.chart.width = kwargs['width']
    if 'height' in kwargs:
        chart.options.chart.height = kwargs['height']
    if 'kind' in kwargs:
        chart.options.chart.type = kwargs['kind']
    if 'stacking' in kwargs:
        chart.options.plotOptions.series.stacking = kwargs['stacking']


def pandas_plot(df, **kwargs):
    """

    :param df: Pandas dataframe ot numpy array
    :return: Highcharts component
    """
    chart = HighCharts(**kwargs)
    chart.load_json(_s1)
    set_chart_kwargs(chart, kwargs)
    if isinstance(df, pd.DataFrame) or isinstance(df, pd.Series):
        x_data = get_index_data(df, chart)
    else:
        raise TypeError(f'{df} type is not Dataframe or Series')

    if isinstance(df, pd.Series):
        c = Dict()
        c.data = make_pairs_list(x_data, list(df))
        chart.options.series.append(c)
    else:
        for series_name, series_data in df.iteritems():
            # Iterates over columns of dataframe
            # print(series_name, list(series_data))
            # print()
            c = Dict()
            c.name = series_name
            c.data =  make_pairs_list(x_data, list(series_data)) # list(series_data)
            # print(c.data)
            chart.options.series.append(c)

    return chart


def pandas_subplot(df, **kwargs):
    x_data = get_index_data(df)
    chart_list = []
    color_index = 0
    num_colors = len(_high_charts_colors)
    for series_name, series_data in df.iteritems():
        chart = HighCharts(**kwargs)
        chart.load_json(_s1)
        set_chart_kwargs(chart, kwargs)
        chart_type = kwargs.get('kind', None)

        if chart_type in ['histogram']:
            # https://www.highcharts.com/demo/histogram
            chart = histogram_chart(chart, series_name, series_data, color_index)
            color_index = (color_index + 1) % 10

        else:
            c = Dict()
            c.name = series_name
            c.data = make_pairs_list(x_data, list(series_data))  # list(series_data)
            c.color = _high_charts_colors[color_index]
            color_index = (color_index + 1) % 10
            chart.options.series.append(c)
        chart_list.append(chart)
    return chart_list

def histogram_chart(chart, series_name, series_data, color_index):
    c = Dict()
    chart.options.legend.layout = 'horizontal'
    chart.options.legend.align = 'center'
    chart.options.xAxis = []
    chart.options.xAxis.append(Dict({'title': {'text': 'Data'}, 'alignTicks': False}))
    chart.options.xAxis.append(Dict({'title': {'text': 'Histogram'}, 'alignTicks': False, 'opposite': True}))
    chart.options.yAxis = []
    chart.options.yAxis.append(Dict({'title': {'text': 'Data'}}))
    chart.options.yAxis.append(Dict({'title': {'text': 'Histogram'}, 'opposite': True}))
    c.type = 'histogram'
    c.name = 'Histogram'
    c.xAxis = 1
    c.yAxis = 1
    c.baseSeries = 's1'
    c.zIndex = -1
    c.color = _high_charts_colors[color_index]
    color_index = (color_index + 1) % 10
    chart.options.series.append(c)
    c = Dict()
    c.id = 's1'
    c.data = list(series_data)
    c.type = 'scatter'
    c.marker.radius = 1.5
    c.color = _high_charts_colors[color_index]
    color_index = (color_index + 1) % 10
    # c.visible = False
    c.name = series_name
    chart.options.series.append(c)
    return chart
