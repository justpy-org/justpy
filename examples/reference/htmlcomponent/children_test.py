# Justpy Tutorial demo children_test from docs/reference/htmlcomponent.md
import justpy as jp

def children_test():
    wp = jp.WebPage()
    div_classes = 'm-2 p-2 bg-blue-500 text-white text-lg'
    span_classes = 'm-2 p-2 bg-blue-500 text-yellow-700 text-xl'
    jp.Div(children=[jp.Div(classes=div_classes, children=
                            [jp.Span(text='s1', classes=span_classes), jp.Span(text='s2', classes=span_classes)])
        ,jp.Div(text='d2', classes=div_classes), jp.Div(text='d3', classes=div_classes), jp.Div(text='d4', classes=div_classes)], a=wp)

    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("children_test",children_test)
