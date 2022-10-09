# Justpy Tutorial demo form_test from docs/tutorial/form.md
import justpy as jp
button_classes = 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded m-2'
input_classes = 'border m-2 p-2'

session_data = {}

def form_test():
    wp = jp.WebPage()
    wp.display_url = '/fill_form'
    
    form1 = jp.Form(a=wp, classes='border m-1 p-1 w-64')

    user_label = jp.Label(text='User Name', classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in1 = jp.Input(placeholder='User Name', a=form1, classes='form-input')
    user_label.for_component = in1

    password_label = jp.Label(classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2 mt-2', a=form1)
    jp.Div(text='Password', classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=password_label)
    jp.Input(placeholder='Password', a=password_label, classes='form-input', type='password')

    check_label = jp.Label(classes='text-sm block', a=form1)
    jp.Input(type='checkbox', a=check_label, classes='form-checkbox text-blue-500')
    jp.Span(text='Send me stuff', a=check_label, classes= 'ml-2')
    submit_button = jp.Input(value='Submit Form', type='submit', a=form1, classes=button_classes)

    def submit_form(self, msg):
        print(msg)
        msg.page.redirect = '/form_submitted'
        session_data[msg.session_id] = msg.form_data

    form1.on('submit', submit_form)

    return wp

@jp.SetRoute('/form_submitted')
def form_submitted(request):
    wp = jp.WebPage()
    wp.display_url = '/thanks'
    jp.Div(text='Thank you for submitting the form', a=wp, classes='text-xl m-2 p-2')
    for field in session_data[request.session_id]:
        if field.type in ['text', 'password']:
            jp.Div(text=f'{field.placeholder}:  {field.value}', a=wp, classes='text-lg m-1 p-1')
        elif field.type == 'checkbox' and field.checked:
            jp.Div(text='We will send you stuff', a=wp, classes='text-lg m-1 p-1')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("form_test",form_test)
