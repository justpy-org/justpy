import justpy as jp
import pandas as pd
import itertools

# https://www.dataquest.io/blog/making-538-plots/
# http://www.randalolson.com/2014/06/14/percentage-of-bachelors-degrees-conferred-to-women-by-major-1970-2012/

wm = pd.read_csv('https://elimintz.github.io/women_majors.csv')
wm_under_20 = list(wm.loc[0, wm.loc[0] < 20].index) # Create list of majors which start under 20%


def make_pairs_list(x_data, y_data):
    return list(map(list, itertools.zip_longest(x_data, y_data)))


def women_majors():
    wp = jp.WebPage()
    wm_chart = jp.HighCharts(a=wp, classes='m-2 p-2 border w-3/4')
    o = wm_chart.options  # Will save us some typing and make code cleaner
    o.title.text = 'The gender gap is transitory - even for extreme cases'
    o.title.align = 'left'
    o.xAxis.title.text = 'Year'
    o.xAxis.gridLineWidth = 1
    o.yAxis.title.text = '% Women in Major'
    o.yAxis.labels.format = '{value}%'
    o.legend.layout = 'proximate'
    o.legend.align = 'right'
    o.series = []
    x_data = wm.iloc[:, 0].tolist()
    for major in wm_under_20:
        s = jp.Dict()
        y_data = wm[major].tolist()
        s.data = make_pairs_list(x_data, y_data)
        s.name = major
        s.type = 'spline'
        o.series.append(s)
        s.marker.enabled = False
    return wp

jp.justpy(women_majors)

#https://query1.finance.yahoo.com/v7/finance/quote?symbols=msft
#https://query1.finance.yahoo.com/v8/finance/chart/msft
#https://query1.finance.yahoo.com/v8/finance/chart/AAPL?symbol=AAPL&period1=0&period2=9999999999&interval=3mo
# https://stackoverflow.com/questions/44030983/yahoo-finance-url-not-working
# https://finance.yahoo.com/quote/AAPL/history?period1=1104555600&period2=1293771600&interval=1d&filter=history&frequency=1d