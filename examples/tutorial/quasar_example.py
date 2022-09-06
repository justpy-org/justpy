"""
Created on 2022-08-27

@author: wf

see https://justpy.io/quasar_tutorial/introduction/
"""
import justpy as jp
import random


async def my_click(self, msg):
    self.color = random.choice(
        [
            "primary",
            "secondary",
            "accent",
            "dark",
            "positive",
            "negative",
            "info",
            "warning",
        ]
    )
    self.label = self.color
    msg.page.dark = not msg.page.dark
    await msg.page.set_dark_mode(msg.page.dark)


def quasar_example():
    wp = jp.QuasarPage(dark=True)  # Load page in dark mode
    d = jp.Div(classes="q-pa-md q-gutter-sm", a=wp)
    jp.QBtn(color="primary", icon="mail", label="On Left", a=d, click=my_click)
    jp.QBtn(color="secondary", icon_right="mail", label="On Right", a=d, click=my_click)
    jp.QBtn(
        color="red",
        icon="mail",
        icon_right="send",
        label="On Left and Right",
        a=d,
        click=my_click,
    )
    jp.Br(a=d)
    jp.QBtn(
        icon="phone",
        label="Stacked",
        stack=True,
        glossy=True,
        color="purple",
        a=d,
        click=my_click,
    )
    return wp


from examples.basedemo import Demo

Demo("quasar example", quasar_example)
