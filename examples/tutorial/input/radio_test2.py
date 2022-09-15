# Justpy Tutorial demo radio_test2 from docs/tutorial/input.md
import justpy as jp


def radio_changed(self, msg):
    self.result_div.text = ''
    d = jp.Div(a=self.result_div, classes='m-2 p-2 border')
    for btn in self.btn_list:
        if btn.checked:
            jp.Span(text=f'{btn.value} is checked', a=d, classes='text-green-500 mr-6')
        else:
            jp.Span(text=f'{btn.value} is NOT checked', a=d, classes='text-red-500 mr-6')


def radio_test2():
    wp = jp.WebPage()
    genders = ['male', 'female', 'other']
    ages = [(0, 30), (31, 60), (61, 100)]

    outer_div = jp.Div(classes='border m-2 p-2 w-64', a=wp)
    # Create div to show radio button selection but don't add yet to page. It will be added at the end
    # It is created here so that it could be assigned to the radio button attribute result_div
    result_div = jp.Div(text='Click radio buttons to see results here', classes='m-2 p-2 text-xl')

    jp.P(a=outer_div, text='Please select your gender:')
    gender_list = []
    for gender in genders:
        label = jp.Label(classes='inline-block mb-1 p-1', a=outer_div)
        radio_btn = jp.Input(type='radio', name='gender', value=gender, a=label, btn_list=gender_list,
                             result_div=result_div, change=radio_changed)
        gender_list.append(radio_btn)
        jp.Span(classes='ml-1', a=label, text=gender.capitalize())

    jp.Div(a=outer_div, classes='m-2')  # Add spacing and line break

    jp.P(a=outer_div, text='Please select your age:')
    age_list = []
    for age in ages:
        label = jp.Label(classes='inline-block mb-1 p-1', a=outer_div)
        radio_btn = jp.Input(type='radio', name='age', value=age[0], a=label, btn_list=age_list,
                             result_div=result_div, change=radio_changed)
        age_list.append(radio_btn)
        jp.Span(classes='ml-1', a=label, text=f'{age[0]} - {age[1]}')
        jp.Br(a=outer_div)

    wp.add(result_div)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("radio_test2",radio_test2)
