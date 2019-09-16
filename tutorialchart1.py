import justpy as jp

# Try http://127.0.0.1:8000/ + one of the entries in charts,
charts = ['org', 'bubbles', 'item', 'timeline', 'states', 'browsers', 'bbb']

@jp.SetRoute('/{chart_name}')
async def chart_test(request):
    wp = jp.WebPage()
    chart_name = request.path_params.get('chart_name', 'item')   # Default chart is item
    print(chart_name)
    if chart_name not in charts:
        chart_name = 'item'
    if chart_name == 'bbb':
        print('correct one')
        r = await jp.get(f'https://elimintz.github.io/charts/{chart_name}')
        print('hello')
        print(r)
        # r = jp.Dict(r)
        print(r)
    else:
        r = await jp.get(f'https://elimintz.github.io/charts/{chart_name}', 'text')
    my_chart = jp.HighCharts(a=wp, classes='m-2 p-2 border w-3/4', options=r)
    return wp

jp.justpy(chart_test)

# s1 = 'https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/goog-c.json'
# data = await jp.get('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/new-intraday.json')
