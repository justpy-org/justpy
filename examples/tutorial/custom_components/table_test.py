# Justpy Tutorial demo table_test from docs/tutorial/custom_components.md
import justpy as jp
import pandas as pd


class AutoTable(jp.Table):

    td_classes = 'border px-4 py-2 text-center'
    tr_even_classes = 'bg-gray-100 '
    tr_odd_classes = ''
    th_classes = 'px-4 py-2'

    def __init__(self, **kwargs):
        self.values = []
        super().__init__(**kwargs)


    def react(self,data):
        self.set_class('table-auto')
        #First row of values is header
        if self.values:
            headers = self.values[0]
            thead = jp.Thead(a=self)
            tr = jp.Tr(a=thead)
            for item in headers:
                jp.Th(text=item, classes=self.th_classes, a=tr)
            tbody = jp.Tbody(a=self)
            for i, row in enumerate(self.values[1:]):
                if i % 2 == 1:
                    tr = jp.Tr(classes=self.tr_even_classes, a=tbody)
                else:
                    tr = jp.Tr(classes=self.tr_odd_classes, a=tbody)
                for item in row:
                    jp.Td(text=item, classes=self.td_classes, a=tr)


wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
wm_df['Year'] = wm_df['Year'].astype('str')
headers = list(wm_df.columns)
table_data = wm_df.to_numpy().tolist()
table_data.insert(0, headers)

def table_test():
    wp = jp.WebPage()
    d = jp.Div(classes='w-7/8 m-2 p-3 border rounded-lg ', a=wp)
    AutoTable(values=table_data, a=d, classes='block p-4 overflow-auto', style='height: 90vh')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("table_test",table_test)
