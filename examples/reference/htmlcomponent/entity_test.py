# Justpy Tutorial demo entity_test from docs/reference/htmlcomponent.md
import justpy as jp

def entity_test():
    wp = jp.WebPage()
    jp.Space(num=3, a=wp)
    jp.HTMLEntity(entity='a&#768;',a=wp, classes='text-lg')
    jp.Span(text='a&#768;',a=wp, classes='text-lg', html_entity=True)
    jp.Space(num=5, a=wp)
    jp.HTMLEntity(entity='a&#769',a=wp, classes='text-xl')
    jp.Span(text='a&#769',a=wp, classes='text-xl', html_entity=True)
    jp.Space(num=5, a=wp)
    jp.HTMLEntity(entity='&#8707;',a=wp, classes='text-2xl')
    jp.Span(text='&#8707;',a=wp, classes='text-2xl', html_entity=True)
    jp.Space(num=5, a=wp)
    jp.HTMLEntity(entity='&copy;', a=wp, classes='text-3xl')
    jp.Span(text='&copy;', a=wp, classes='text-3xl', html_entity=True)
    jp.Space(num=5, a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("entity_test",entity_test)
