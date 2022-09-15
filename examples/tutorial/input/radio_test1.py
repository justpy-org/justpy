# Justpy Tutorial demo radio_test1 from docs/tutorial/input.md
import justpy as jp

def radio_test1():
    wp = jp.WebPage()
    genders = ['male', 'female', 'other']
    ages = [(0, 30), (31, 60), (61, 100)]

    outer_div = jp.Div(classes='border m-2 p-2 w-64', a=wp)

    jp.P(a=outer_div, text='Please select your gender:')
    for gender in genders:
        label = jp.Label(classes='inline-block mb-1 p-1', a=outer_div)
        radio_btn = jp.Input(type='radio', name='gender', value=gender, a=label)
        jp.Span(classes='ml-1', a=label, text=gender.capitalize())

    jp.Div(a=outer_div, classes='m-2')  # Add spacing and line break
    jp.P(a=outer_div, text='Please select your age:')
    for age in ages:
        label = jp.Label(classes='inline-block mb-1 p-1', a=outer_div)
        radio_btn = jp.Input(type='radio', name='age', value=age[0], a=label)
        jp.Span(classes='ml-1', a=label, text=f'{age[0]} - {age[1]}')
        jp.Br(a=outer_div)

    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("radio_test1",radio_test1)
