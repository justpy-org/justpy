import justpy as jp

# Example from https://www.highcharts.com/docs/getting-started/your-first-chart
my_chart_def1 = """
{
        chart: {
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
}
"""

my_chart_def = """
{
    

    series: [{
        data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
    }]
}
"""

my_chart_def = """
{
    chart: {
        type: 'line'
    },

    title: {
        text: 'Basic shape annotations'
    },

    series: [{
        keys: ['y', 'id'],
        data: [[29.9, '0'], [71.5, '1'], [106.4, '2'], [129.2, '3'], [144.0, '4'], [176.0, '5']]
    }],

    yAxis: {
        max: 300
    },

    xAxis: {
        min: 0,
        max: 6
    },

    annotations: [{
        shapes: [{
            point: '0',
            type: 'circle',
            r: 10
        }, {
            point: '3',
            type: 'rect',
            width: 20,
            height: 20,
            x: -10,
            y: -25
        }, {
            fill: 'none',
            stroke: 'red',
            strokeWidth: 3,
            type: 'path',
            points: ['0', '3', {
                x: 6,
                y: 195,
                xAxis: 0,
                yAxis: 0
            }],
            markerEnd: 'arrow'
        }],
        labels: [{
            point: {
                x: 6,
                y: 195,
                xAxis: 0,
                yAxis: 0
            }
        }]
    }]
}
"""

def click_point(self, msg):
    print(msg.selected_points)
    print(msg)
    print(msg.accumulate)
    print(f'Points selected {len(msg.selected_points)}')
    self.d.text = f'x: {msg.x}, y: {msg.y}, category: {msg.category}'
    self.d.style = f'color: {msg.color};'

def my_click(self, msg):
    print('jjj')
    print(msg)
    # self.text = ' clicked'
    return
    msg.page.add(jp.Div(text='Chart click!'))

def my_series_hide(self, msg):
    print(msg)

def chart_test():
    wp = jp.WebPage()
    d1 = jp.Div(a=wp, text='hell', style='height: 100px')
    d2 = jp.Div(a=wp)
    my_chart = jp.HighCharts(a=d2, classes='m-2 p-2 border', style='width: 600px')
    my_chart.options = my_chart_def
    d = jp.Div(text='point info will go here', classes='m-2 p-2 text-2xl', a=wp)
    my_chart.d = d
    my_chart.options.series[0].allowPointSelect = True
    my_chart.on('series_hide', my_series_hide)
    my_chart.on('series_show', my_series_hide)
    my_chart.on('series_click', my_series_hide)
    # my_chart.event_propagation = False
    # my_chart.options.series[1].allowPointSelect = True
    my_chart.on('point_select', click_point)
    my_chart.on('point_unselect', click_point)
    d1.on('click', my_click)
    d2.on('click', my_click)
    return wp

jp.justpy(chart_test)
