import justpy as jp
import pandas as pd

iris = pd.read_csv(
    "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
)
iris_stats = iris.describe().round(3)
iris_stats.insert(loc=0, column="stats", value=iris_stats.index)
iris_species = list(iris["species"].unique())

# Create a dictionary of frames per iris species
iris_species_frames = {}
for s in iris_species:
    iris_species_frames[s] = iris.loc[iris["species"] == s]


async def click_point(self, msg):
    # print(msg)
    return await self.select_point(
        [
            {"id": chart_id, "series": msg.series_index, "point": msg.point_index}
            for chart_id in self.chart_list
            if self.id != chart_id
        ],
        msg.websocket,
    )


async def tooltip_formatter(self, msg):
    # print(msg)
    tooltip_html = f"""
    <div style="color: {msg.color}"><span>&#x25CF;</span> {msg.series_name}</div>
    <div style="color: {msg.color}">{self.col1}: {msg.x}</div>
    <div style="color: {msg.color}">{self.col2}: {msg.y}</div>
    """
    await self.draw_crosshair(
        [
            {"id": chart_id, "series": msg.series_index, "point": msg.point_index}
            for chart_id in self.chart_list
        ],
        msg.websocket,
    )
    return await self.tooltip_update(tooltip_html, msg.websocket)


def iris_data():
    wp = jp.WebPage(highcharts_theme="gray", title="Iris Dataset", debug=True)
    jp.Div(
        text="Iris Dataset",
        classes="text-3xl m-2 p-2 font-medium tracking-wider text-yellow-300 bg-gray-800 text-center",
        a=wp,
    )
    d1 = jp.Div(classes="m-2 p-2 border-2", a=wp)
    chart_list = []
    for i, col1 in enumerate(iris.columns[:4]):
        d2 = jp.Div(classes="flex", a=d1)
        for j, col2 in enumerate(iris.columns[:4]):
            if i != j:  # Not on the diagonal
                chart = jp.HighCharts(
                    a=d2, style="width: 300px; height: 300px", classes="flex-grow m-1"
                )
                chart_list.append(chart.id)
                chart.chart_list = chart_list
                chart.on("tooltip", tooltip_formatter)
                chart.tooltip_y = 85
                chart.on("point_click", click_point)
                chart.col1 = col1
                chart.col2 = col2
                o = chart.options
                o.chart.type = "scatter"
                o.chart.zoomType = "xy"
                o.title.text = ""
                o.legend.enabled = False
                o.credits.enabled = (
                    False if i < 3 or j < 3 else True
                )  # https://api.highcharts.com/highcharts/credits.enabled
                o.xAxis.title.text = col2 if i == 3 else ""
                o.yAxis.title.text = col1 if j == 0 else ""
                o.xAxis.crosshair = o.yAxis.crosshair = True
                for k, v in iris_species_frames.items():
                    s = jp.Dict()
                    s.name = k
                    s.allowPointSelect = True  # https://api.highcharts.com/highcharts/series.scatter.allowPointSelect
                    s.marker.states.select.radius = 8
                    s.data = list(zip(v.iloc[:, j], v.iloc[:, i]))
                    o.series.append(s)
            else:
                chart = jp.Histogram(
                    list(iris.iloc[:, j]),
                    a=d2,
                    style="width: 300px; height: 300px",
                    classes="flex-grow m-1",
                )
                o = chart.options
                o.title.text = ""
                o.legend.enabled = False
                o.xAxis[0].title.text = col2 if i == 3 else ""
                o.xAxis[1].title.text = ""
                o.yAxis[0].title.text = col1 if j == 0 else ""
                o.yAxis[1].title.text = ""
                o.credits.enabled = False if i < 3 or j < 3 else True

    # Add two grids, first with the data and second with statistics describing the data
    iris.jp.ag_grid(
        a=wp,
        classes="m-2 p-2",
        style="height: 500px; width: 800px",
        auto_size=True,
        theme="ag-theme-balham-dark",
    )
    iris_stats.jp.ag_grid(
        a=wp,
        classes="m-2 p-2 border",
        style="height: 500px; width: 950px",
        auto_size=True,
        theme="ag-theme-material",
    )
    return wp


from examples.basedemo import Demo

Demo("iris demo", iris_data, HIGHCHARTS=True, AGGRID=True)
