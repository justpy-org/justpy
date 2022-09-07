# Justpy Tutorial demo rating_test1 from docs/quasar_tutorial/QRating.md
import justpy as jp


def rating_test1():
    wp = jp.QuasarPage(data={"rating": 2})
    d = jp.Div(classes="q-pa-md", a=wp)
    rating_div = jp.Div(classes="q-gutter-y-md column", a=d)
    jp.QRating(size="1.5em", icon="thumb_up", a=rating_div, model=[wp, "rating"])
    jp.QRating(
        size="2em",
        icon="favorite_border",
        color="red-7",
        a=rating_div,
        model=[wp, "rating"],
    )
    jp.QRating(
        size="2.5em",
        icon="create",
        color="purple-4",
        a=rating_div,
        model=[wp, "rating"],
    )
    jp.QRating(
        size="3em", icon="pets", color="brown-5", a=rating_div, model=[wp, "rating"]
    )
    jp.QRating(
        size="4.5em",
        icon="star_border",
        color="green-5",
        a=rating_div,
        model=[wp, "rating"],
    )
    jp.QRating(
        size="5em",
        icon="star_border",
        icon_selected="star",
        color="grey",
        a=rating_div,
        model=[wp, "rating"],
        color_selected=[
            "light-green-3",
            "light-green-6",
            "green",
            "green-9",
            "green-10",
        ],
    )
    jp.QRating(
        size="5em",
        icon="star_border",
        icon_selected="star",
        color="green-5",
        a=rating_div,
        model=[wp, "rating"],
    )
    jp.QRating(
        size="3.5em",
        max=4,
        color="red-5",
        a=rating_div,
        model=[wp, "rating"],
        icon=[
            "sentiment_very_dissatisfied",
            "sentiment_dissatisfied",
            "sentiment_satisfied",
            "sentiment_very_satisfied",
        ],
    )
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("rating_test1", rating_test1)
