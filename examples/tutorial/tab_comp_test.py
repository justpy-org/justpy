"""
Created on 2022-08-24

@author: em
https://justpy.io/tutorial/custom_components/#tab-group-component
"""
import justpy as jp
from justpy import Div
from examples.tutorial.tab_group_component import Tabs, TabsPills

my_chart_def = """
{
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Fruit Consumption'
        },
        xAxis: {
            categories: ['Apples', 'Bananas', 'Oranges']
        },
        yAxis: {
            title: {
                text: 'Fruit eaten'
            }
        },
        series: [{
            name: 'Jane',
            data: [1, 0, 4],
            animation: false
        }, {
            name: 'John',
            data: [5, 7, 3],
            animation: false
        }]
}
"""
# https://dog.ceo/api/breed/papillon/images/random
pics_french_bulldogs = ["5458", "7806", "5667", "4860"]
pics_papillons = ["5037", "2556", "7606", "8241"]


def tab_change(self, msg):
    print("in change", msg)


def tab_comp_test():
    wp = jp.WebPage(data={"tab": "id2556"})

    t = Tabs(a=wp, classes="w-3/4 m-4", style="", animation=True, content_height=550)
    for chart_type in ["bar", "column", "line", "spline"]:
        d = jp.Div(style=Tabs.wrapper_style, delete_flag=True)
        my_chart = jp.HighCharts(
            a=d,
            classes="m-2 p-2 border",
            style="width: 1000px;",
            options=my_chart_def,
            use_cache=False,
        )
        my_chart.options.chart.type = chart_type
        my_chart.options.title.text = f"Chart of Type {chart_type.capitalize()}"
        my_chart.options.subtitle.text = f"Subtitle {chart_type.capitalize()}"
        t.add_tab(f"id{chart_type}", f"{chart_type}", d)

    d_flex = Div(classes="flex", a=wp)  # Container for the two dog pictures tabs

    t = Tabs(
        a=d_flex,
        classes=" w-1/2 m-4",
        animation=True,
        content_height=550,
        model=[wp, "tab"],
        change=tab_change,
    )
    for pic_id in pics_papillons:
        d = jp.Div(style=Tabs.wrapper_style)
        jp.Img(
            src=f"https://images.dog.ceo/breeds/papillon/n02086910_{pic_id}.jpg", a=d
        )
        t.add_tab(f"id{pic_id}", f"Pic {pic_id}", d)

    t = TabsPills(
        a=d_flex,
        classes="w-1/2 m-4",
        animation=True,
        content_height=550,
        change=tab_change,
    )
    for pic_id in pics_french_bulldogs:
        d = jp.Div(style=Tabs.wrapper_style)
        jp.Img(
            src=f"https://images.dog.ceo/breeds/bulldog-french/n02108915_{pic_id}.jpg",
            a=d,
        )
        t.add_tab(f"id{pic_id}", f"Pic {pic_id}", d)

    input_classes = "w-1/3 m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    in1 = jp.Input(classes=input_classes, model=[wp, "tab"], a=wp)

    return wp


from examples.basedemo import Demo

Demo("tabgroup test", tab_comp_test)
