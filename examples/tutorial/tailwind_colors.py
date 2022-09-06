# see https://justpy.io/tutorial/tailwind/
import justpy as jp


def text_colors():
    wp = jp.WebPage()
    d = jp.Div(classes="flex flex-wrap m-2", a=wp)
    for color in jp.Tailwind.tw_dict["text_color"]:
        jp.Div(
            text=color,
            classes=f"{color} font-mono p-1 text-lg bg-blue-100 hover:bg-red-500 w-48",
            a=d,
        )
    return wp


from examples.basedemo import Demo

Demo("tailwind colors demo", text_colors)
