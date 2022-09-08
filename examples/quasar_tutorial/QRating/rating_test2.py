# Justpy Tutorial demo rating_test2 from docs/quasar_tutorial/QRating.md
import justpy as jp


def rating_test2():
    wp = jp.QuasarPage()
    wp.tailwind = True
    num_stars = 3
    r = jp.QRating(
        size="2em",
        max=num_stars,
        color="primary",
        classes="m-2 p-2",
        a=wp,
        value=2,
        debounce=0,
    )
    for i in range(1, num_stars + 1, 1):
        t = jp.QTooltip(text=f"{i} rating")
        r.add_scoped_slot(f"tip-{i}", t)
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("rating_test2", rating_test2)
