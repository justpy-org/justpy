import justpy as jp
import pandas as pd
import numpy as np
import asyncio

# https://worldhappiness.report/ed/2019/
df = pd.read_csv("http://elimintz.github.io/happiness_report_2019.csv").round(3)


def grid_change(self, msg):
    msg.page.df = jp.read_csv_from_string(msg.data)
    c = msg.page.df.jp.plot(
        "Country",
        msg.page.cols_to_plot,
        kind="column",
        title="World Happiness Ranking",
        subtitle="Click and drag in the plot area to zoom in. Shift + drag to pan",
        stacking=msg.page.stacking,
        temp=True,
    )
    msg.page.c.options = c.options


def stack_change(self, msg):
    msg.page.c.options.plotOptions.series.stacking = self.value
    msg.page.stacking = self.value


def series_change(self, msg):
    msg.page.cols_to_plot = []
    for i, toggle in enumerate(msg.page.toggle_list):
        if toggle.value:
            msg.page.cols_to_plot.append(i + 3)
    c = msg.page.df.jp.plot(
        "Country",
        msg.page.cols_to_plot,
        kind="column",
        title="World Happiness Ranking",
        subtitle="Click and drag in the plot area to zoom in. Shift + drag to pan",
        stacking=msg.page.stacking,
        temp=True,
    )
    msg.page.c.options = c.options


async def corr_button_click(self, msg):
    msg.page.open = "/corr"
    await msg.page.update()
    msg.page.open = ""
    return True


def happiness_plot(request):
    # ['Country', 'Rank', 'Score', 'Unexplained', 'GDP', 'Social_support', 'Health', 'Freedom', 'Generosity', Corruption']
    wp = jp.QuasarPage()
    chart_theme = request.query_params.get("theme", 8)  # Default is 'grid'
    themes = [
        "high-contrast-dark",
        "high-contrast-light",
        "avocado",
        "dark-blue",
        "dark-green",
        "dark-unica",
        "gray",
        "grid-light",
        "grid",
        "sand-signika",
        "skies",
        "sunset",
    ]
    wp.highcharts_theme = themes[int(chart_theme)]
    wp.stacking = ""
    wp.cols_to_plot = [3, 4, 5, 6, 7, 8, 9]
    wp.df = df
    d = jp.Div(classes="q-ma-lg", a=wp)
    bg = jp.QBtnToggle(
        push=True,
        glossy=True,
        toggle_color="primary",
        value="",
        a=d,
        input=stack_change,
        style="margin-right: 30px",
    )
    bg.options = [
        {"label": "No Stacking", "value": ""},
        {"label": "Normal", "value": "normal"},
        {"label": "percent", "value": "percent"},
    ]
    wp.toggle_list = []
    corr_button = jp.QBtn(
        label="Show pairwise correlation", a=d, click=corr_button_click
    )
    for i in df.columns[3:]:
        wp.toggle_list.append(
            jp.QToggle(
                checked_icon="check",
                color="green",
                unchecked_icon="clear",
                value=True,
                label=f"{i}",
                a=d,
                input=series_change,
            )
        )  # ,style='margin-right: 10px',
    chart = df.jp.plot(
        "Country",
        wp.cols_to_plot,
        kind="column",
        a=wp,
        title="World Happiness Ranking",
        subtitle="Click and drag in the plot area to zoom in. Shift + drag to pan",
        stacking="",
        classes="border m-2 p-2 q-ma-lg p-ma-lg",
    )
    grid = df.jp.ag_grid(a=wp)
    grid.options.columnDefs[0].rowDrag = True
    for event_name in ["sortChanged", "filterChanged", "columnMoved", "rowDragEnd"]:
        grid.on(event_name, grid_change)
    wp.c = chart
    grid.c = chart
    bg.c = chart
    return wp


class ScatterWithRegression(jp.Scatter):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, **kwargs)
        x = np.asarray(x)
        y = np.asarray(y)
        m = (len(x) * np.sum(x * y) - np.sum(x) * np.sum(y)) / (
            len(x) * np.sum(x * x) - np.sum(x) ** 2
        )
        b = (np.sum(y) - m * np.sum(x)) / len(x)
        s = jp.Dict()  # The new series
        s.type = "line"
        s.marker.enabled = False
        s.enableMouseTracking = False
        min = float(x.min())
        max = float(x.max())
        s.data = [[min, m * min + b], [max, m * max + b]]
        s.name = f"Regression, m: {round(m, 3)}, b: {round(b, 3)}"
        self.options.series.append(s)


chart_list = []


def create_corr_page():
    # creates a page showing correlation between factors
    score_factors = [
        "Unexplained",
        "GDP",
        "Social_support",
        "Health",
        "Freedom",
        "Generosity",
        "Corruption",
    ]
    wp = jp.WebPage(delete_flag=False)
    d = jp.Div(a=wp, classes="flex flex-wrap")
    for x_col in score_factors:
        for y_col in score_factors[score_factors.index(x_col) + 1 :]:
            x = df[x_col]
            y = df[y_col]
            chart = ScatterWithRegression(
                x,
                y,
                a=d,
                style="width: 400px; height: 400px; margin: 10px;",
                classes="border",
            )
            chart_list.append(chart)
            o = chart.options
            o.title.text = f"{x_col} vs. {y_col}"
            o.xAxis.title.text = x_col
            o.yAxis.title.text = y_col
            o.tooltip.pointFormat = f"{{point.country}}<br/></b>{x_col}: <b>{{point.x}}</b><br/></b>{y_col}: <b>{{point.y}}</b><br/>"
            o.tooltip.useHtml = True
            o.series[0].name = f"{x_col} vs. {y_col}"
            data = []
            # Make the first series data a dictionary so that the country name  will be available to the tooltip
            for i, point in enumerate(o.series[0].data):
                data.append({"x": point[0], "y": point[1], "country": df["Country"][i]})
            o.series[0].data = data
    corr_def = (
        df[
            [
                "Unexplained",
                "GDP",
                "Social_support",
                "Health",
                "Freedom",
                "Generosity",
                "Corruption",
            ]
        ]
        .corr()
        .round(3)
    )
    corr_def.insert(loc=0, column="Factors/Factors", value=corr_def.index)
    g = corr_def.jp.ag_grid(a=wp, style="width: 90%; height: 250px", classes="m-2")
    return wp


corr_page = create_corr_page()


@jp.SetRoute("/corr")
def corr_test():
    return corr_page


async def page_ready(self, msg):
    wp = msg.page
    for chart in chart_list:
        wp.d.add(chart)
        await self.update()
        await asyncio.sleep(0.5)


# Loads charts one by one to page, improving user experience
@jp.SetRoute("/corr_staggered")
def corr_stag_test():
    wp = jp.WebPage()
    wp.on("page_ready", page_ready)
    wp.d = jp.Div(a=wp, classes="flex flex-wrap")
    return wp


from examples.basedemo import Demo

Demo("happiness plot demo", happiness_plot)
