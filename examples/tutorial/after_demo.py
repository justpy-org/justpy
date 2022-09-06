import justpy as jp

btn_classes = jp.Styles.button_outline + " m-2"
notification_classes = "m-2 text-center text-xl bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded w-64"


def btn_click(self, msg):
    self.nl[self.list_index].show = True


def btn_after(self, msg):
    self.nl[self.list_index].show = False


def after_demo():
    wp = jp.WebPage()
    btn_list = []
    notification_list = []

    for index, btn_text in enumerate(["First", "Second", "Third"]):
        btn_list.append(
            jp.Button(
                text=f"{btn_text} Button",
                classes=btn_classes,
                a=wp,
                nl=notification_list,
                list_index=index,
                click=btn_click,
                after=btn_after,
            )
        )

    for notification_text in ["First", "Second", "Third"]:
        notification_list.append(
            jp.Div(
                text=f"{notification_text} Notification",
                classes=notification_classes,
                a=wp,
                show=False,
            )
        )

    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("after demo", after_demo)
