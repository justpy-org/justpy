# Justpy Tutorial demo grid_test from docs/tutorial/custom_components.md
import justpy as jp
import pandas as pd

class LinkedChartGrid(jp.Div):

    def __init__(self, df, x, y, **kwargs):
        super().__init__(**kwargs)
        self.df = df
        self.x = x
        self.y = y
        self.kind = kwargs.get('kind', 'column')
        self.stacking = kwargs.get('stacking', '')
        self.title = kwargs.get('title', '')
        self.subtitle = kwargs.get('subtitle', '')
        self.set_classes('flex flex-col')
        self.chart = df.jp.plot(x, y, a=self, classes='m-2 p-2 border', kind=self.kind, stacking=self.stacking, title=self.title, subtitle=self.subtitle)
        self.grid = df.jp.ag_grid(a=self)
        self.grid.parent = self
        for event_name in ['sortChanged', 'filterChanged', 'columnMoved', 'rowDragEnd']:
            self.grid.on(event_name, self.grid_change)


    @staticmethod
    def grid_change(self, msg):
        self.parent.df = jp.read_csv_from_string(msg.data)
        c = self.parent.df.jp.plot(self.parent.x, self.parent.y, kind=self.parent.kind, title=self.parent.title,
                                   subtitle=self.parent.subtitle, stacking=self.parent.stacking)
        self.parent.chart.options = c.options



alcohol_df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/alcohol-consumption/drinks.csv', encoding="ISO-8859-1")
bad_drivers_df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/bad-drivers/bad-drivers.csv', encoding="ISO-8859-1")


def grid_test():
    wp = jp.WebPage()
    c = LinkedChartGrid(alcohol_df, 0, [1,2,3,4], kind='column', a=wp, classes='m-4 p-2 border',
                        stacking='normal', title='Alcohol Consumption per Country', subtitle='538 data')
    LinkedChartGrid(bad_drivers_df, 0, [1,2,3,4,5,6,7], kind='column', a=wp, classes='m-4 p-2 border-4', title='Bad Drivers per US State', subtitle='538 data')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("grid_test",grid_test)
