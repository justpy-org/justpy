#!/usr/bin/env python3
import justpy as jp

wp = jp.WebPage()
wp.add(jp.Div(text="Hello, world!"))

from examples.basedemo import Demo

Demo("Issue 469", lambda: wp)
