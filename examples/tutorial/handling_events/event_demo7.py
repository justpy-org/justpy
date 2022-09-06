# Justpy Tutorial demo event_demo7 from docs/tutorial/handling_events.md
import justpy as jp


def button_click3(self, msg):
    self.num_clicked += 1
    # self.message.text = f'{self.text} clicked. Number of clicks: {self.num_clicked}'
    p = jp.P(text=f"{self.text} clicked. Number of clicks: {self.num_clicked}")
    self.message.add_component(p, 0)
    for button in msg.page.button_list:
        button.set_class("bg-blue-500")
        button.set_class("bg-blue-700", "hover")
    self.set_class("bg-red-500")
    self.set_class("bg-red-700", "hover")


def event_demo7():
    number_of_buttons = 25
    wp = jp.WebPage()
    button_div = jp.Div(classes="flex m-4 flex-wrap", a=wp)
    button_classes = "w-32 mr-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
    message = jp.Div(classes="text-lg border m-2 p-2 overflow-auto h-64", a=wp)
    message.add(jp.P(text="No button clicked yet"))
    button_list = []
    for i in range(1, number_of_buttons + 1):
        b = jp.Button(
            text=f"Button {i}",
            a=button_div,
            classes=button_classes,
            click=button_click3,
        )
        b.message = message
        b.num_clicked = 0
        button_list.append(b)
    wp.button_list = (
        button_list  # The list will now be referenced by the WebPage instance attribute
    )
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("event_demo7", event_demo7)
