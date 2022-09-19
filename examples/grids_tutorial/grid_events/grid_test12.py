# Justpy Tutorial demo grid_test12 from docs/grids_tutorial/grid_events.md
import justpy as jp
import pandas as pd

wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def row_selected3(self, msg):
    print(msg)
    if msg.selected:
        categories, values = list(msg.data.keys()), list(msg.data.values())
        o = self.row_chart.options
        o.title.text = f'{values[0]} - Percent Women in Major'
        o.xAxis.categories = categories[1:]
        s = jp.Dict({'name': values[0], 'data': values[1:]})
        s.dataLabels.enabled = True
        if len(o.series) > 0:
            o.series[0] = s
        else:
            o.series.append(s)
        self.row_selected3 = msg.rowIndex
        self.row_chart.show = True
    elif self.row_selected3 == msg.rowIndex:
        self.row_chart.show = False

def grid_test12():
    wp = jp.WebPage()
    row_chart = jp.HighCharts(a=wp)
    row_chart.options.chart.type = 'column'
    row_chart.options.yAxis.title.text = '%'
    row_chart.show = False
    grid = wm_df.jp.ag_grid(a=wp)
    grid.row_chart = row_chart
    grid.on('rowSelected', row_selected3)
    grid.options.columnDefs[0].checkboxSelection = True
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("grid_test12",grid_test12)
