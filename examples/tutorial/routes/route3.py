# Justpy Tutorial demo  from docs/tutorial/routes.md
import justpy as jp


def greeting_function(request):
    wp = jp.WebPage()
    name = f"""{request.path_params["name"]}"""
    wp.add(jp.P(text=f"Hello there, {name}!", classes="text-5xl m-2"))
    return wp


jp.Route("/hello/{name}", greeting_function)

# initialize the demo
from examples.basedemo import Demo

Demo("route3", None)
