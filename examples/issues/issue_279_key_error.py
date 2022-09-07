# see https://github.com/justpy-org/justpy/issues/279
import justpy as jp
import time


def button_click(self, _msg):
    """
    on button click delete the components of the button
    """
    self.num_clicked += 1
    self.message.text = f"{self.text} clicked. Number of clicks: {self.num_clicked}"
    self.set_class("bg-red-500")
    self.set_class("bg-red-700", "hover")
    self.button_div.delete_components()
    # wait a bit so that another button may be clicked
    time.sleep(3)


def issue_279():
    """
    show misbehavior of handle_events when a message for a non existing component arrives
    """
    number_of_buttons = 25
    wp = jp.WebPage()
    button_div = jp.Div(classes="flex m-4 flex-wrap", a=wp)
    button_classes = "w-32 mr-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
    message = jp.Div(
        text="No button clicked yet", classes="text-2xl border m-4 p-2", a=wp
    )
    for i in range(1, number_of_buttons + 1):
        b = jp.Button(
            text=f"Button {i}",
            a=button_div,
            classes=button_classes,
            click=button_click,
            button_div=button_div,
        )
        b.message = message
        b.num_clicked = 0
    return wp


from examples.basedemo import Demo

Demo("Issue 279 KeyError", issue_279)
