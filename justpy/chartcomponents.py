from .htmlcomponents import *
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
import demjson
from addict import Dict
#TODO: May need to call chart.reflow() on resize

#use Box on graph options? https://github.com/cdgriffith/Box
#Use addict https://github.com/mewwts/addict

#If width of chart not specified it defaults to 600px
# A JavaScript date is fundamentally specified as the number of milliseconds that have elapsed since midnight on January 1, 1970, UTC
# https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/UTC
# https://www.npmtrends.com/highcharts-vs-plotly

class Point:
   # x, y, color eventually marker

    def __init__(self,  **kwargs):


        for k, v in kwargs.items():
            self.__setattr__(k,v)


class HighCharts(JustpyBaseComponent):

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
        super().__init__(**kwargs)
        # self.html_tag = 'div'
        self.vue_type = 'chart'
        self.running_id = 0
        for k, v in kwargs.items():
            self.__setattr__(k,v)
        self.allowed_events = ['tooltip', 'point_click']
        if type(self.options) != Dict:
            self.options = Dict(self.options)
        for com in ['a', 'add_to']:
            if com in kwargs.keys():
                kwargs[com].add_component(self)

    def __repr__(self):
        return f'{self.__class__.__name__}(id: {self.id}, vue_type: {self.vue_type}, chart options: {self.options})'

    async def update(self):
        try:
            websocket_dict = WebPage.sockets[self.page_id]
        except:
            return self
        component_build = self.build_list()
        for websocket in websocket_dict.values():
            # await websocket.send_json({'type': 'page_update', 'data': self.build_list()})
            try:
                # await websocket.send_json({'type': 'page_update', 'data': component_build})  # Change to create task?
                WebPage.loop.create_task(websocket.send_json({'type': 'page_update', 'data': component_build})) # Change to create task?
            except:
                print('Problem with websocket in page update, ignoring')
        return self

    async def tooltip_update(self, tooltip, websocket):
        await websocket.send_json({'type': 'tooltip_update', 'data': tooltip, 'id': self.id})
        # So the page itself does not update, only the tooltip
        return True

    async def example_on_tooltip(self, msg):
        # https://api.highcharts.com/highcharts/tooltip.formatter
        print(msg)
        websocket_dict = WebPage.sockets[msg.page.page_id]
        await asyncio.sleep(0.2)
        for websocket in websocket_dict.values():
            await websocket.send_json({'type': 'tooltip_update', 'data': f'<span style="font-size:20px">helloblah {msg.series_name} {msg.x} {msg.y}</span>', 'id': msg.id})
        return {'type': 'tooltip_update', 'data': '<span style="font-size:20px">hello</span>', }

    def delete(self):
        if not self.pages and self.delete_flag:
            super().delete()
            # JustpyBaseComponent.instances.pop(self.id, None)

    def add_to_page(self, wp: WebPage):
        wp.add_component(self)

    def add_to(self, *args):
        for c in args:
            c.add_component(self)

    def react(self, data):
        pass

    def load_json(self, options_string):
        """

        :param options_string: A string describing the the graph as it would in Javascript as an object. It is JSON like
        :return: An addict type namsapce that can be acccessed through dot notation https://github.com/mewwts/addict
        """

        self.options = Dict(demjson.decode(options_string.encode("ascii", "ignore")))
        # self.options = Dict(demjson.decode(options_string))
        return self.options


    def load_json_from_file(self, file_name):
        with open(file_name,'r') as f:
            self.options = Dict(demjson.decode(f.read().encode("ascii", "ignore")))
        return self.options

    def convert_object_to_dict(self):

        d = {}
        d['vue_type'] = self.vue_type
        d['id'] = self.id
        # d['running_id'] = self.id
        d['stock'] = self.stock
        d['show'] = self.show
        d['classes'] = self.classes
        d['style'] = self.style
        d['def'] = self.options
        d['events'] = self.events
        return d

class HighStock(HighCharts):

    # This is a component that other components can be added to

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.stock = True