# https://github.com/elimintz/justpy/issues/387
# https://justpy.io/tutorial/custom_components/#tab-group-component
import justpy as jp
from examples.tutorial.tab_group_component import Tabs, TabsPills
import pandas as pd


def tab_comp_test():

    wp = jp.WebPage()

    dfs = [
        pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}),
        pd.DataFrame({"bb": range(10), "cc": range(10)}),
        pd.DataFrame(
            {
                "foo": [1001, 1002, 1003, 1004],
                "bar": range(4),
                "blah": [1234, 2345, 3456, 4567],
            }
        ),
        pd.DataFrame({"c1": range(7), "c2": range(7)}),
    ]

    t = Tabs(a=wp, classes="w-3/4 m-4", style="", animation=False, content_height=550)
    for idx, chart_type in enumerate(["bar", "column", "line", "spline"]):
        d = jp.Div(style=Tabs.wrapper_style, delete_flag=True)
        l = jp.Label(a=d, text=chart_type)
        dfs[idx].jp.ag_grid(a=d, style="width: 100%")
        t.add_tab(f"id{chart_type}", f"{chart_type}", d)

    return wp


from examples.basedemo import Demo

Demo("Issue 387 aggrid tabgroup", tab_comp_test)
