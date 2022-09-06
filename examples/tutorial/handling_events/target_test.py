# Justpy Tutorial demo target_test from docs/tutorial/handling_events.md
import justpy as jp


class ButtonDiv(jp.Div):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        for i in range(1, 6):
            b = jp.Button(
                text=f"Button {i}", a=self, classes=" m-2 p-2 border text-blue text-lg"
            )
            b.num = i
            b.on("click", self.button_clicked)
        self.info_div = jp.Div(
            text="info will go here", classes="m-2 p-2 border", a=self
        )

    def button_clicked(self, msg):
        print(self)
        print(msg.target)
        self.info_div.text = f"Button {msg.target.num} was clicked"


def target_test():
    wp = jp.WebPage()
    ButtonDiv(a=wp)
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("target_test", target_test)
