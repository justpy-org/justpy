import hjson

from .htmlcomponents import *
from addict import Dict
import itertools
from urllib.parse import quote


# TODO: May need to call chart.reflow() on resize
# TODO: Handle formatter functions, for example in dataLabels and others.
# TODO: Add support for more events like drilldown

# If width of chart not specified it defaults to 600px
# A JavaScript date is fundamentally specified as the number of milliseconds that have elapsed since midnight on January 1, 1970, UTC
# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/UTC


def make_pairs_list(x_data, y_data):
    return list(map(list, itertools.zip_longest(x_data, y_data)))


class HighCharts(JustpyBaseComponent):
    # Highcharts.getOptions().colors
    highcharts_colors = [
        "#7cb5ec",
        "#434348",
        "#90ed7d",
        "#f7a35c",
        "#8085e9",
        "#f15c80",
        "#e4d354",
        "#2b908f",
        "#f45b5b",
        "#91e8e1",
    ]

    # Theme is One of ['avocado', 'dark-blue', 'dark-green', 'dark-unica', 'gray',
    # 'grid-light', 'grid', 'high-contrast-dark', 'high-contrast-light', 'sand-signika', 'skies', 'sunset']
    # but is set at the WebPage level. All charts on same page have the same theme.
    # Example: wp.highcharts_theme = 'grid'

    vue_type = "chart"  # The corresponding Vue component

    chart_types = [
        "columnrange",
        "cylinder",
        "dependencywheel",
        "errorbar",
        "funnel",
        "funnel3d",
        "gauge",
        "heatmap",
        "histogram",
        "item",
        "line",
        "networkgraph",
        "organization",
        "packedbubble",
        "pareto",
        "pie",
        "polygon",
        "pyramid",
        "pyramid3d",
        "sankey",
        "scatter",
        "scatter3d",
        "solidgauge",
        "spline",
        "streamgraph",
        "sunburst",
        "tilemap",
        "timeline",
        "treemap",
        "variablepie",
        "variwide",
        "vector",
        "venn",
        "waterfall",
        "windbarb",
        "wordcloud",
        "xrange",
    ]

    def __init__(self, **kwargs):
        self.options = Dict()
        self.stock = False
        self.use_cache = True
        self.classes = ""
        self.style = ""
        self.show = True
        self.event_propagation = True
        self.pages = {}
        self.tooltip_fixed = False
        self.tooltip_x = -40
        self.tooltip_y = 40
        self.tooltip_debounce = 100  # Default is 100 ms
        self.update_animation = True  # Whether to animate changes when chart is updated
        self.update_create = False  # Whether to create new chart on update, if false current chart is updated
        kwargs["temp"] = False  # Force an id to be assigned to chart
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        self.allowed_events = [
            "tooltip",
            "point_click",
            "point_select",
            "point_unselect",
            "series_hide",
            "series_show",
            "series_click",
            "zoom_x",
            "zoom_y",
        ]
        for e in self.allowed_events:
            for prefix in ["", "on", "on_"]:
                if prefix + e in kwargs.keys():
                    fn = kwargs[prefix + e]
                    if isinstance(fn, str):
                        fn_string = f"def oneliner{self.id}(self, msg):\n {fn}"
                        exec(fn_string)
                        self.on(e, locals()[f"oneliner{self.id}"])
                    else:
                        self.on(e, fn)
                    break
        if type(self.options) != Dict:
            self.options = Dict(self.options)
        if "series" not in self.options:
            self.options.series = []
        for com in ["a", "add_to"]:
            if com in kwargs.keys():
                kwargs[com].add_component(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(id: {self.id}, vue_type: {self.vue_type}, chart options: {self.options})"

    def __setattr__(self, key, value):
        if key == "options":
            if isinstance(value, str):
                self.load_json(value)
            else:
                super().__setattr__(key, value)
        else:
            super().__setattr__(key, value)

    async def chart_update(self, update_dict, websocket):
        # https://api.highcharts.com/class-reference/Highcharts.Chart#update
        await websocket.send_json(
            {"type": "chart_update", "data": update_dict, "id": self.id}
        )
        # So the page itself does not update, only the tooltip, return True not None
        return True

    async def tooltip_update(self, tooltip, websocket):
        await websocket.send_json(
            {"type": "tooltip_update", "data": tooltip, "id": self.id}
        )
        # So the page itself does not update, only the tooltip, return True not None
        return True

    async def draw_crosshair(self, point_list, websocket):
        """
        point_list is list of dictionaries  whose keys are:
        'id': the chart id
        'series': the series index
        'point': the point index
        Values are  all integers
        Example:
         {'id': chart_id, 'series': msg.series_index, 'point': msg.point_index}
        """
        await websocket.send_json({"type": "draw_crosshair", "data": point_list})
        # Return True not None so that the page does not update
        return True

    async def select_point(self, point_list, websocket):
        """
        point_list is list of of dictionaries  whose keys are:
        'id': the chart id
        'series': the series index
        'point': the point index
        Values are  all integers
        Example:
         {'id': chart_id, 'series': msg.series_index, 'point': msg.point_index}
        """
        await websocket.send_json({"type": "select_point", "data": point_list})
        # Return True not None so that the page does not update
        return True

    def add_to_page(self, wp: WebPage):
        wp.add_component(self)

    def add_to(self, *args):
        for c in args:
            c.add_component(self)

    def react(self, data):
        pass

    def load_json(self, options_string):
        self.options = Dict(hjson.loads(options_string.encode("ascii", "ignore")))
        return self.options

    def load_json_from_file(self, file_name):
        with open(file_name, "r") as f:
            self.options = Dict(hjson.loads(f.read().encode("ascii", "ignore")))
        return self.options

    def convert_object_to_dict(self):

        d = {}
        d["vue_type"] = self.vue_type
        d["id"] = self.id
        d["stock"] = self.stock
        d["use_cache"] = self.use_cache
        d["show"] = self.show
        d["classes"] = self.classes
        d["style"] = self.style
        d["event_propagation"] = self.event_propagation
        d["def"] = self.options
        d["events"] = self.events
        d["tooltip_fixed"] = self.tooltip_fixed
        d["tooltip_x"] = self.tooltip_x
        d["tooltip_y"] = self.tooltip_y
        d["tooltip_debounce"] = self.tooltip_debounce
        d["update_animation"] = self.update_animation
        d["update_create"] = self.update_create
        return d


class HighStock(HighCharts):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stock = True


class Histogram(HighCharts):
    _options = """
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
        self.load_json(self._options)
        self.options.series[1].data = list(data)


class Pie(HighCharts):
    _options = """
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
        self.load_json(self._options)
        series = Dict()
        series.type = "pie"
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
        self.options.series.append(series)


class PieSemiCircle(HighCharts):
    _options = """
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
        self.labels = []
        super().__init__(**kwargs)
        self.load_json(self._options)
        series = Dict()
        series.type = "pie"
        series.innerSize = "60%"
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
        self.options.series.append(series)


class Scatter(HighCharts):
    _options = """
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
        self.load_json(self._options)
        s = Dict()
        s.data = list(zip(x, y))
        self.options.series.append(s)


# --------------------------------------------------------------------
# matplotlib related objects

try:
    import matplotlib.pyplot as plt

    _has_matplotlib = True
    import io
except:
    _has_matplotlib = False

if _has_matplotlib:

    class Matplotlib(Div):
        def __init__(self, **kwargs):
            self.figure = plt.gcf()
            super().__init__(**kwargs)
            self.set_figure(self.figure)

        def set_figure(self, fig=None):
            if not fig:
                fig = self.figure
            plt.figure(fig.number)
            output = io.StringIO()
            plt.savefig(output, format="svg")
            # The 'white-space:pre' causes problems in placement of chart on page
            self.inner_html = output.getvalue().replace(
                "*{stroke-linecap:butt;stroke-linejoin:round;white-space:pre;}",
                "*{stroke-linecap:butt;stroke-linejoin:round;}",
            )
            output.close()
            return self.inner_html


# --------------------------------------------------------------------
# deck.gl related objects

s = """
<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><iframe src="about:blank" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" data-html={} onload="this.contentDocument.open();this.contentDocument.write(    decodeURIComponent(this.getAttribute('data-html')));this.contentDocument.close();" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>
"""

try:
    import pydeck as pdk

    _has_pydeck = True
except:
    _has_pydeck = False

if _has_pydeck:

    class PyDeckFrame(Iframe):
        vue_type = "iframejp"

        def __init__(self, **kwargs):
            self.deck = None
            self.srcdoc = None
            kwargs["temp"] = False  # Force an id to be assigned to chart
            self.view_delay = (
                0  # Additional delay in ms for display after frame has loaded
            )
            self.transition_duration = (
                0.1  # Duration of transition between frames in seconds
            )
            super().__init__(**kwargs)

        def convert_object_to_dict(self):
            self.srcdoc = quote(self.deck.to_html(as_string=True))
            d = super().convert_object_to_dict()
            d["view_delay"] = self.view_delay
            d["transition_duration"] = self.transition_duration
            return d

    class PyDeck(Div):
        vue_type = "deckgl"

        def __init__(self, **kwargs):
            self.use_cache = False
            self.deck = None
            kwargs["temp"] = False  # Force an id to be assigned to chart
            super().__init__(**kwargs)

        def convert_object_to_dict(self):
            d = {}
            d["vue_type"] = self.vue_type
            d["id"] = self.id
            d["use_cache"] = self.use_cache
            d["show"] = self.show
            d["classes"] = self.classes
            d["style"] = self.style
            d["event_propagation"] = self.event_propagation
            d["deck"] = self.deck.to_json()
            d["events"] = self.events
            d["mapbox_key"] = self.deck.mapbox_key
            return d


try:
    import altair as alt

    _has_altair = True
except:
    _has_altair = False

if _has_altair:

    class AltairChart(Div):

        vue_type = "altairjp"

        def __init__(self, **kwargs):
            self.use_cache = False
            self.chart = None
            self.options = {}
            self.vega_source = None
            # self.style = 'width:100%; height: 500px'
            kwargs["temp"] = False  # Force an id to be assigned to chart
            super().__init__(**kwargs)

        def convert_object_to_dict(self):
            d = {}
            d["vue_type"] = self.vue_type
            d["id"] = self.id
            d["use_cache"] = self.use_cache
            d["show"] = self.show
            d["classes"] = self.classes
            d["style"] = self.style
            d["event_propagation"] = self.event_propagation
            if self.vega_source:
                d["vega_source"] = json.dumps(self.vega_source)
            else:
                d["vega_source"] = self.chart.to_json()
            d["events"] = self.events
            d["options"] = self.options
            return d


try:
    import plotly

    _has_plotly = True
except:
    _has_plotly = False

if _has_plotly:

    class PlotlyChart(Div):

        vue_type = "plotlyjp"

        def __init__(self, **kwargs):
            self.use_cache = False
            self.chart = None
            self.chart_dict = {}
            self.config = {}
            kwargs["temp"] = False  # Force an id to be assigned to chart
            super().__init__(**kwargs)

        def convert_object_to_dict(self):
            d = {}
            d["vue_type"] = self.vue_type
            d["id"] = self.id
            d["use_cache"] = self.use_cache
            d["show"] = self.show
            d["classes"] = self.classes
            d["style"] = self.style
            d["event_propagation"] = self.event_propagation
            if self.chart:
                d["chart"] = self.chart.to_json()
            else:
                d["chart"] = self.chart_dict
            d["events"] = self.events
            d["config"] = self.config
            return d


try:
    import bokeh

    _has_bokeh = True
except:
    _has_bokeh = False

if _has_bokeh:

    class BokehChart(Div):

        vue_type = "bokehjp"

        def __init__(self, **kwargs):
            self.use_cache = False
            self.chart = None
            self.chart_dict = {}
            self.config = {}
            kwargs["temp"] = False  # Force an id to be assigned to chart
            super().__init__(**kwargs)

        def convert_object_to_dict(self):
            d = {}
            d["vue_type"] = self.vue_type
            d["id"] = self.id
            d["use_cache"] = self.use_cache
            d["show"] = self.show
            d["classes"] = self.classes
            d["style"] = self.style
            d["event_propagation"] = self.event_propagation
            if self.chart:
                d["chart"] = json.dumps(bokeh.embed.standalone.json_item(self.chart))
            else:
                d["chart"] = self.chart_dict
            d["events"] = self.events
            d["config"] = self.config
            return d


try:
    import folium

    _has_folium = True
except:
    _has_folium = False

if _has_folium:

    class FoliumChart(Div):
        def __init__(self, **kwargs):
            self.use_cache = False
            self.chart = None
            kwargs["temp"] = False  # Force an id to be assigned to chart
            super().__init__(**kwargs)
            self.inner_div = Div(a=self)

        def convert_object_to_dict(self):
            if self.chart:
                self.inner_html = self.chart._repr_html_()
            d = super().convert_object_to_dict()
            return d
