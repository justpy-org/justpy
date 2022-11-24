# Justpy Tutorial demo create_chart_test5 from docs/charts_tutorial/creating_charts.md
import justpy as jp

# https://github.com/elimintz/elimintz.github.io/tree/master/charts
# Try https://127.0.0.1:8000/ + any one of the entries in charts
# For example: http://127.0.0.1:8000/bubbles
charts = ["org", "bubbles", "item", "timeline", "states", "browsers", "wheel"]


@jp.SetRoute("/demo/create_chart_test5/{chart_name}")
async def create_chart_test5(request):
    wp = jp.WebPage()
    chart_name = request.path_params.get("chart_name", "item")   # Default chart is item
    if chart_name not in charts:
        chart_name = "item"
    chart_options = await jp.get(f"https://elimintz.github.io/charts/{chart_name}", "text")
    my_chart = jp.HighCharts(a=wp, classes="m-2 p-2 border w-3/4", options=chart_options)
    return wp

# initialize the demo
from examples.basedemo import Demo
Demo("create_chart_test5", create_chart_test5)
