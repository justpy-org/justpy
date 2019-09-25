import justpy as jp
import pandas as pd

iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
iris_stats = iris.describe().round(3)
iris_stats.insert(loc=0, column='stats', value=iris_stats.index)
iris_species = list(iris['species'].unique())
iris_species_frames = {}
# Create a dictionary of dataframes per iris species
for s in iris_species:
    iris_species_frames[s] = iris.loc[iris['species'] == s]

async def click_point(self, msg):
    print(msg)
    return await self.select_point([{'id': chart_id, 'series': msg.series_index, 'point': msg.point_index} for chart_id in self.chart_list if self.id != chart_id], jp.get_websocket(msg))


async def tooltip_formatter(self, msg):
    print(msg)
    tooltip_html = f"""
    <div><span class="bg-white" style="color: {msg.color}">&#x25CF;</span> {msg.series_name}</div>
    <div>{self.col1}: {msg.x}</div>
    <div>{self.col2}: {msg.y}</div>
    """
    await self.draw_crosshair([{'id': chart_id, 'series': msg.series_index, 'point': msg.point_index} for chart_id in self.chart_list], jp.get_websocket(msg))
    # await self.select_point([{'id': chart_id, 'series': msg.series_index, 'point': msg.point_index} for chart_id in self.chart_list], jp.get_websocket(msg))
    return await self.tooltip_update(tooltip_html, jp.get_websocket(msg))


def test_pd():
    wp = jp.WebPage()
    jp.Div(text='Iris Dataset', classes='text-3xl m-2 p-2 text-white bg-blue-600 text-center', a=wp)
    d1 = jp.Div(classes='m-2 p-2 border-2', a=wp)
    chart_list = []
    for i, col1 in enumerate(iris.columns[:4]):
        d2 = jp.Div(classes='flex', a=d1)
        for j, col2 in enumerate(iris.columns[:4]):
            if i != j:     # Not on the diagonal
                chart = jp.HighCharts(a=d2, style='width: 300px; height: 300px', classes='flex-grow m-1 p-3')
                chart_list.append(chart.id)
                chart.chart_list = chart_list
                chart.on('tooltip', tooltip_formatter)
                chart.on('point_click', click_point)
                chart.col1 = col1
                chart.col2 = col2
                o = chart.options
                o.chart.type = 'scatter'
                o.chart.zoomType = 'xy'
                o.title.text = ''
                o.legend.enabled = False
                o.credits.enabled = False if i<3 or j<3 else True
                o.xAxis.title.text = col2 if i==3 else ''
                o.yAxis.title.text = col1 if j==0 else ''
                o.xAxis.crosshair = True
                o.yAxis.crosshair = True
                o.tooltip.headerFormat = '<b>{series.name}</b><br>'
                o.series = []
                for k, v in iris_species_frames.items():
                    serie = jp.Dict()
                    serie.name = k
                    serie.allowPointSelect = True
                    serie.marker.states.select.radius = 8
                    serie.data = list(zip(v.iloc[:, j], v.iloc[:, i]))
                    o.series.append(serie)
            else:
                chart = jp.Histogram(list(iris.iloc[:, j]),a=d2, style='width: 300px; height: 300px', classes='flex-grow m-1 p-3')
                o = chart.options
                o.title.text = ''
                o.legend.enabled = False
                o.xAxis[0].title.text = col2 if i==3 else ''
                o.xAxis[1].title.text = ''
                o.yAxis[0].title.text = col1 if j == 0 else ''
                o.yAxis[1].title.text = ''
                o.credits.enabled = False if i < 3 or j < 3 else True

    grid = jp.AgGrid(a=wp, classes='m-2 p-2', style='height: 500px; width: 800px', auto_size=True, theme='ag-theme-balham-dark')
    grid.load_pandas_frame(iris)
    grid_stats = jp.AgGrid(a=wp, classes='m-2 p-2 border', style='height: 500px; width: 950px', auto_size=True, theme='ag-theme-material')
    grid_stats.load_pandas_frame(iris_stats)
    return wp

jp.justpy(test_pd, websockets=True)
