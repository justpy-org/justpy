# Justpy Tutorial demo qdrawer_page from docs/quasar_tutorial/quasar_components.md
"""
Quasar Drawer example see https://github.com/justpy-org/justpy/issues/589
"""
import justpy as jp


def toggle_visible_drawer(self, msg):
    self.drawer.value = not self.drawer.value


def qdrawer_page():
    wp = jp.QuasarPage()

    btn_drawer = jp.QBtn(
        flat=True,
        round=True,
        dense=True,
        icon="menu",
        a=wp,
        click=toggle_visible_drawer,
    )

    wp_layout = jp.QLayout(a=wp)
    PageContainer = jp.QPageContainer(a=wp_layout)
    pageText = jp.Div(a=PageContainer, text="page container")

    drawer = jp.QDrawer(
        width=200,
        breakpoint=500,
        bordered=True,
        a=wp_layout,
    )
    btn_drawer.drawer = drawer
    ScrollArea = jp.QScrollArea(classes="fit", a=drawer)
    c2 = jp.Div(a=ScrollArea, text="scroll area left")

    return wp

# initialize the demo
from examples.basedemo import Demo
Demo("qdrawer_page", qdrawer_page)
