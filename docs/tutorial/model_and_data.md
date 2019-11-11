# The Model and Data Attributes
The model attribute is a special one in JustPy. You don't need to use it, but if you do, it may make your code more concise and readable. 
Try running the following program and typing into the input field in the browser:
import justpy as jp

async def input_demo(request):
    wp = jp.WebPage(data={ 'text': 'Initial text'})
    input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded xtw-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
    jp.Input(a=wp, classes=input_classes, placeholder='Please type here', model=[wp, 'text'])
    jp.Div(model=[wp, 'text'], classes='m-2 p-2 h-32 text-xl border-2 overflow-auto', a=wp)
    return wp

jp.justpy(input_demo)

Its functionality is the same as examples above. Text entered in an input field is reflected in a div on the page. The connection between the input and the div is made using the model and data attributes. Notice that when we create the web page, we gave it a data attribute. The data attribute must be a Python dict. In our case it is a dict with one entry. The key is 'text' and the value is 'Initial text'. 
When we create the Input element, we have added the following to its keyword arguments: model=[wp, 'text']
This tells the Input instance that it will model itself based on the value under the 'text' key in wp's data. For an Input element this means that when rendered it will take its value from wp.data['text']  AND when its value is changed due to an input event, it will set wp.data['text'] to its value. It is important to understand that in the case of Input, model has a two way influence. It gets its value from the appropriate data attribute and when an input event occurs it changes the appropriate data attribute.
In the case of a Div element the relation is only one way. Its text attribute is rendered according to the model attribute but it does not change the data dict ever.
If an element has an input event, the model attribute works in two directions, otherwise just in one. For two directional elements the attribute changed is value while for one directional ones the attribute changed is text.
How is this useful? Let's put three divs on the page instead of just one:
import justpy as jp

async def input_demo(request):
    wp = jp.WebPage(data={'text': 'Initial text'})
    input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded xtw-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
    jp.Input(a=wp, classes=input_classes, placeholder='Please type here', model=[wp, 'text'])
    for _ in range(3):
        jp.Div(model=[wp, 'text'], classes='m-2 p-2 h-32 text-xl border-2 overflow-auto', a=wp)
    return wp

jp.justpy(input_demo)

Since all Divs have the same model, they change when we type. Without the model attribute, implementing this would be more verbose.
Now let's duplicate the Inputs. Let's have five Inputs instead of one:
import justpy as jp

async def input_demo(request):
    wp = jp.WebPage(data={'text': 'Initial text'})
    input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded xtw-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
    for _ in range(5):
        jp.Input(a=wp, classes=input_classes, placeholder='Please type here', model=[wp, 'text'])
    for _ in range(3):
        jp.Div(model=[wp, 'text'], classes='m-2 p-2 h-32 text-xl border-2 overflow-auto', a=wp)
    return wp

jp.justpy(input_demo)

Type into any one of the five Input fields and see what happens. Since all elements share the same model, they all change in tandem. We didn't need to write any event handler.
Let's make a small modification to the program and add a reset button that will clear all the elements on the page:
import justpy as jp

async def input_demo(request):
    wp = jp.WebPage(data={'text': 'Initial text'})
    button_classes = 'w-32 m-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
    b = jp.Button(text='Reset', click=" msg.page.data['text'] = '' ", a=wp, classes=button_classes)
    jp.Hr(a=wp)  # Add horizontal like to page
    input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded xtw-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
    for _ in range(5):
        jp.Input(a=wp, classes=input_classes, placeholder='Please type here', model=[wp, 'text'])
    for _ in range(3):
        jp.Div(model=[wp, 'text'], classes='m-2 p-2 h-32 text-xl border-2 overflow-auto', a=wp)
    return wp

jp.justpy(input_demo)

When the button is clicked, the following command is executed: msg.page.data['text'] = ''
Since all the Inputs and Divs are modeled after this dict entry, they are all reset to the empty string when the button is clicked. 
Any element, a Div for example, may have a data attribute and be used in a model attribute, not just a WebPage. 
