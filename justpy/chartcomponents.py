from .htmlcomponents import *
import demjson
from addict import Dict
import itertools

#TODO: May need to call chart.reflow() on resize
#TODO: Handle formatter functions, for example in dataLabels and others.
#TODO: Add support for events like drilldown
#TODO: Add support for drawCrosshair https://api.highcharts.com/class-reference/Highcharts.Axis#drawCrosshair and tooltip refresh

# If width of chart not specified it defaults to 600px
# A JavaScript date is fundamentally specified as the number of milliseconds that have elapsed since midnight on January 1, 1970, UTC
# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/UTC

def make_pairs_list(x_data, y_data):
    return list(map(list, itertools.zip_longest(x_data, y_data)))

class HighCharts(JustpyBaseComponent):

    # Highcharts.getOptions().colors
    highcharts_colors = ["#7cb5ec", "#434348", "#90ed7d", "#f7a35c", "#8085e9", "#f15c80", "#e4d354", "#2b908f", "#f45b5b", "#91e8e1"]

    #Theme is Ooe of ['avocado', 'dark-blue', 'dark-green', 'dark-unica', 'gray',
    #'grid-light', 'grid', 'high-contrast-dark', 'high-contrast-light', 'sand-signika', 'skies', 'sunset']
    # but is set at the WebPage level. All charts on same page have the same theme.
    # Example: wp.highcharts_theme = 'grid'

    vue_type = 'chart'
    chart_types = ['columnrange', 'cylinder', 'dependencywheel', 'errorbar', 'funnel', 'funnel3d', 'gauge', 'heatmap',
                   'histogram', 'item', 'line', 'networkgraph', 'organization', 'packedbubble', 'pareto', 'pie',
                   'polygon', 'pyramid', 'pyramid3d', 'sankey', 'scatter', 'scatter3d', 'solidgauge',
                   'spline', 'streamgraph', 'sunburst', 'tilemap', 'timeline', 'treemap', 'variablepie', 'variwide',
                   'vector', 'venn', 'waterfall', 'windbarb', 'wordcloud', 'xrange']

    def __init__(self, **kwargs):
        self.options = Dict()
        self.stock = False
        self.classes = ''
        self.style = ''
        self.show = True
        self.pages = {}
        self.tooltip_fixed = False
        self.tooltip_x = -40
        self.tooltip_y = 40
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            self.__setattr__(k,v)
        self.allowed_events = ['tooltip', 'point_click']
        for e in self.allowed_events:
            for prefix in ['', 'on', 'on_']:
                if prefix + e in kwargs.keys():
                    fn = kwargs[prefix + e]
                    if isinstance(fn, str):
                        fn_string = f'def oneliner{self.id}(self, msg):\n {fn}'
                        exec(fn_string)
                        self.on(e, locals()[f'oneliner{self.id}'])
                    else:
                        self.on(e, fn)
                    break
        if type(self.options) != Dict:
            self.options = Dict(self.options)
        for com in ['a', 'add_to']:
            if com in kwargs.keys():
                kwargs[com].add_component(self)

    def __repr__(self):
        return f'{self.__class__.__name__}(id: {self.id}, vue_type: {self.vue_type}, chart options: {self.options})'

    def __setattr__(self, key, value):
        if key == 'options':
            if isinstance(value, str):
                self.load_json(value)
            else:
                self.__dict__[key] = value
        else:
            self.__dict__[key] = value


    async def tooltip_update(self, tooltip, websocket):
        await websocket.send_json({'type': 'tooltip_update', 'data': tooltip, 'id': self.id})
        # So the page itself does not update, only the tooltip, return True not None
        return True

    async def draw_crosshair(self, point_list, websocket):
        # data is list of od dict with keys id, series, point all integers
        # {'id': chart_id, 'series': msg.series_index, 'point': msg.point_index}
        await websocket.send_json({'type': 'draw_crosshair', 'data': point_list})
        # So the page itself does not update, only the tooltip, return True not None
        return True

    async def select_point(self, point_list, websocket):
        # data is list of od dict with keys id, series, point all integers
        # {'id': chart_id, 'series': msg.series_index, 'point': msg.point_index}
        await websocket.send_json({'type': 'select_point', 'data': point_list})
        # So the page itself does not update, only the tooltip, return True not None
        return True

    def add_to_page(self, wp: WebPage):
        wp.add_component(self)

    def add_to(self, *args):
        for c in args:
            c.add_component(self)

    def react(self, data):
        pass

    def load_json(self, options_string):
        self.options = Dict(demjson.decode(options_string.encode("ascii", "ignore")))
        return self.options


    def load_json_from_file(self, file_name):
        with open(file_name,'r') as f:
            self.options = Dict(demjson.decode(f.read().encode("ascii", "ignore")))
        return self.options

    def convert_object_to_dict(self):

        d = {}
        d['vue_type'] = self.vue_type
        d['id'] = self.id
        d['stock'] = self.stock
        d['show'] = self.show
        d['classes'] = self.classes
        d['style'] = self.style
        d['def'] = self.options
        d['events'] = self.events
        d['tooltip_fixed'] = self.tooltip_fixed
        d['tooltip_x'] = self.tooltip_x
        d['tooltip_y'] = self.tooltip_y
        return d


class HighStock(HighCharts):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.stock = True


class Histogram(HighCharts):

    _s1 = """
{
    title: {
        text: 'Highcharts Histogram'
    },
    xAxis: [{
        title: { text: 'Data' },
        alignTicks: false
    }, {
        title: { text: 'Histogram' },
        alignTicks: false,
        opposite: true
    }],

    yAxis: [{
        title: { text: 'Data' }
    }, {
        title: { text: 'Histogram' },
        opposite: true
    }],

    series: [{
        name: 'Histogram',
        type: 'histogram',
        xAxis: 1,
        yAxis: 1,
        baseSeries: 's1',
        zIndex: -1
    }, {
        name: 'Data',
        type: 'scatter',
        data: [],
        id: 's1',
        marker: {
            radius: 1.5
        }
    }]
}

    """

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        chart = self
        chart.load_json(self._s1)
        chart.options.series[1].data = list(data)


class Pie(HighCharts):

    _s1 = """
            {
                chart: {
                    title: {
                        text: 'Pie Chart'
                        }
                    },
                    tooltip: {
                        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                    },
                    plotOptions: {
                        pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            dataLabels: {
                                enabled: true,
                                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                            }
                        }
                    },
                    series: []
            }
                """

    def __init__(self, data, **kwargs):
        self.labels = []
        super().__init__(**kwargs)
        chart = self
        chart.load_json(self._s1)
        series = Dict()
        series.type = 'pie'
        series_data = []
        series.data = series_data
        for i, value in enumerate(data):
            c = Dict()
            try:
                c.name = self.labels[i]
            except:
                c.name = str(value)
            c.y = value
            series_data.append(c)
        chart.options.series.append(series)

class PieSemiCircle(HighCharts):

    _s1 = """
            {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                },
                title: {
            text: 'SemiCircle Chart',
            align: 'center',
            verticalAlign: 'middle',
            y: 40
        },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                plotOptions: {
            pie: {
                dataLabels: {
                    enabled: true,
                    distance: -50,
                    style: {
                        fontWeight: 'bold',
                        color: 'white'
                    }
                },
                startAngle: -90,
                endAngle: 90,
                center: ['50%', '75%'],
                size: '110%'
            }
        },
                series: []
            }
            """

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        chart = self
        chart.load_json(self._s1)
        series = Dict()
        series.type = 'pie'
        series.innerSize = '60%'
        series_data = []
        series.data = series_data
        for i, value in enumerate(data):
            c = Dict()
            try:
                c.name = self.labels[i]
            except:
                c.name = str(value)
            c.y = value
            series_data.append(c)
        chart.options.series.append(series)


class Scatter(HighCharts):
    _s1 = """
    {
    chart: {
        type: 'scatter',
        zoomType: 'xy'
    },
    title: {
        text: 'Scatter Chart'
    },
     xAxis: {
        title: {
            enabled: true,
            text: 'x'
        },
        startOnTick: false,
        endOnTick: true,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'y'
        }
    },
    series:[]
    }
    """

    def __init__(self, x, y, **kwargs):
        super().__init__(**kwargs)
        self.load_json(self._s1)
        s = Dict()
        s.data = list(zip(x,y))
        self.options.series.append(s)


class ScatterWithRegression(Scatter):

    def __init__(self, x, y, **kwargs):
        super().__init__(**kwargs)
        m = (len(x) * np.sum(x * y) - np.sum(x) * np.sum(y)) / (len(x) * np.sum(x * x) - np.sum(x) ** 2)
        b = (np.sum(y) - m * np.sum(x)) / len(x)
        s = jp.Dict()
        s.type = 'line'
        s.marker.enabled = False
        s.enableMouseTracking = False
        min = x.min()
        max = x.max()
        s.data = [[min, m * min + b], [max, m * max + b]]
        s.name = f'Regression, m: {round(m, 3)}, b: {round(b, 3)}'
        o.series.append(s)
