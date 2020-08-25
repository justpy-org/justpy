# QInput

## Introduction

The [Quasar QInput component](https://quasar.dev/vue-components/input) is very versatile and comes with many features and options. Almost all are supported by JustPy.

QInput like Input creates an input event when its value changes.

The program below puts on the page several QInput elements with different features. All are connected using the the same `model` attribute. 

```python
import justpy as jp

def input_test(request):
    wp = jp.QuasarPage(data={'text': ''})
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    c3 = jp.QInput(label='Standard', a=c2, model=[wp, 'text'])
    c4 = jp.QInput(filled=True, label='Filled', a=c2, model=[wp, 'text'])
    c5 = jp.QInput(outlined=True, label='Outlined', a=c2, model=[wp, 'text'])
    c6 = jp.QInput(standout=True, label='Standout', a=c2, model=[wp, 'text'])
    c7 = jp.QInput(standout='bg-teal text-white', label='Custom standout', a=c2, model=[wp, 'text'])
    c8 = jp.QInput(borderless=True, label='Borderless', a=c2, model=[wp, 'text'])
    c9 = jp.QInput(rounded=True, filled=True, label='Rounded filled', a=c2, model=[wp, 'text'])
    c10 = jp.QInput(rounded=True, outlined=True, label='Rounded outlined', a=c2, model=[wp, 'text'])
    c11 = jp.QInput(rounded=True, standout=True, label='Rounded standout', a=c2, model=[wp, 'text'])
    c12 = jp.QInput(square=True, filled=True, label='Square filled', hint='This is a hint', a=c2, model=[wp, 'text'])
    c13 = jp.QInput(square=True, outlined=True, label='Square outlined', a=c2, model=[wp, 'text'])
    c14 = jp.QInput(square=True, standout=True, label='Square standout', a=c2, model=[wp, 'text'])
    return wp

jp.justpy(input_test)
```

## Using Slots

```python
import justpy as jp

def input_test(request):
    wp = jp.QuasarPage()
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    icon1 = jp.QIcon(name='event', color='blue')
    icon2 = jp.QIcon(name='place', color='red')
    for slot in ['append', 'prepend', 'before']:
        in1 = jp.QInput(label=slot, filled=True, hint=f'Icon is in slot "{slot}" and "after"', a=c2, after_slot=icon2)
        #in1.after_slot = icon2    # Alternative to keyword method used in line above
        setattr(in1, slot + '_slot', icon1)
    return wp

jp.justpy(input_test)

```

## Password Visibility Toggle Example

```python
import justpy as jp

def input_test(request):
    wp = jp.QuasarPage()
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)

    password_input = jp.QInput(filled=True,  type='password', a=c2, hint="Password with toggle")
    visibility_icon = jp.QIcon(name='visibility_off', classes='cursor-pointer')
    visibility_icon.password_input = password_input

    password_input.append_slot = visibility_icon

    def toggle_password(self, msg):
        if self.name == 'visibility_off':
            self.name = 'visibility'
            self.password_input.type='text'
        else:
            self.name = 'visibility_off'
            self.password_input.type = 'password'

    visibility_icon.on('click', toggle_password)

    return wp

jp.justpy(input_test)
```

Or better yet, as a reusable component

```python
import justpy as jp

class PasswordWithToggle(jp.QInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'password'
        visibility_icon = jp.QIcon(name='visibility_off', classes='cursor-pointer')
        visibility_icon.password_input = self
        self.append_slot = visibility_icon
        visibility_icon.on('click', self.toggle_password)

    @staticmethod
    def toggle_password(self, msg):
        if self.name == 'visibility_off':
            self.name = 'visibility'
            self.password_input.type = 'text'
        else:
            self.name = 'visibility_off'
            self.password_input.type = 'password'


def input_test(request):
    wp = jp.QuasarPage(data={'text': ''})
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    for i in range(1,6):
        PasswordWithToggle(filled=True,  type='password', a=c2, hint=f'Password with toggle #{i}')
    return wp

jp.justpy(input_test)

```

## Input Masks


```python
import justpy as jp

def input_test(request):
    wp = jp.QuasarPage(data={'text': ''})
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    jp.QInput(filled=True, label='Phone', mask='(###) ### - ####', hint="Mask: (###) ### - ####", a=c2)
    return wp

jp.justpy(input_test)

```

## Input Validation

In the example below, a regular expression is used to validate a field as the user is typing (you of course may use instead any one of the available data validation packages). It uses QInput's `error` and `error_message` props.

```python
import justpy as jp
import re

email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

def input_change(self, msg):
    print(self.value)
    if re.match(email_regex,self.value):
        self.error = False
    else:
        self.error = True
        self.error_message = 'Enter valid email address'
        self.bottom_slots = True


def input_test():
    wp = jp.QuasarPage()
    in1 = jp.QInput(label='Enter email', style='width: 150px; margin: 20px', a=wp, input=input_change)
    return wp


jp.justpy(input_test)
```

You can also use QInput's internal validation prop `rules`. The prop needs to be a list that contains a string that represents JavaScript functions. See the [examples](https://quasar.dev/vue-components/input#Internal-validation) in the Quasar documentation

```python
import justpy as jp

def input_test():
    wp = jp.QuasarPage()
    in1 = jp.QInput(label='Enter email', style='width: 150px; margin: 20px', a=wp, lazy_rules=False)
    in1.rules = ["val => val.length <= 3 || 'Please use maximum 3 characters'"]
    return wp

jp.justpy(input_test)
```

## QInputChange and QInputBlur - Disabling the Input Event

In some cases the debounce feature may not be sufficient to provide a good user experience. This may happen when users type in bursts. Setting debounce to 1000 almost always solves these problems but there is another option if the large debounce is causing other issues. You can disable the input event altogether and capture the value of the QInput when it loses focus.

You can control this yourself by setting the `disable_input_event` attribute to `True` or use the predefined QInputChange and QInputBlur components. QInputBlur will only update the value of the field when the component loses focus. QInputChange will update the value when the change event is fired. Both are very similar except that change will also fire when the Enter key is pressed and focus remains on the component.

The regular QInput component generates an event each time a character is typed into the field. In some case this is not necessary and may put unwanted burden on the server. If you are not implementing a look ahead or validating the field on the server as the user is typing, it is preferable to use QInputChange and QInputBlur instead of QInput. 


```html
import justpy as jp

def my_blur(self, msg):
    self.div.text = self.value

def input_demo(request):
    wp = jp.QuasarPage()
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    in1 = jp.QInputBlur(a=c2,placeholder='Please type here', label='QInputBlur')
    in1.div = jp.Div(text='What you type will show up here only when Input element loses focus',
                      classes='text-h6', a=c2)
    in1.on('blur', my_blur)
    return wp

jp.justpy(input_demo)
```

## Yahoo Stock Charts Example

!!! warning
    You need to install the `pandas-datareader` package to run this example

In the example below we define a component which simplifies entering dates. Click on the calendar icon of the QInput elements to have the a QDate element pop-up.

Using a ticker and the dates provided by the user, data is retrieved from Yahoo and a chart is displayed.

This is also an example of how you would change a Quasar button to the loading state while data is being retrieved. 

```python
import justpy as jp
from pandas_datareader import data as pdr
import datetime
import functools

epoch = datetime.datetime(1970, 1, 1)
grouping_units = [['week', [1]], ['month', [1, 2, 3, 4, 6]]]

chart_dict = {
    'rangeSelector': {'selected': 1},
    'yAxis': [
        {'labels': {'align': 'right', 'x': -3}, 'title': {'text': 'OHLC'}, 'height': '60%', 'lineWidth': 2, 'resize': {'enabled': True}},
        {'labels': {'align': 'right', 'x': -3}, 'title': {'text': 'Volume'}, 'top': '65%', 'height': '35%', 'offset': 0, 'lineWidth': 2}
    ],
    'tooltip': {'split': True},
    'series': [
        {'type': 'candlestick', 'tooltip': {'valueDecimals': 2}, 'dataGrouping': {'units': grouping_units}},
        {'type': 'column', 'name': 'Volume', 'yAxis': 1, 'dataGrouping': {'units': grouping_units}}
    ]
}


class QInputDate(jp.QInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        date_slot = jp.QIcon(name='event', classes='cursor-pointer')
        c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=date_slot)
        self.date = jp.QDate(mask='YYYY-MM-DD', name='date', a=c2)

        self.date.parent = self
        self.date.value = self.value
        self.append_slot = date_slot
        self.date.on('input', self.date_time_change)
        self.on('input', self.input_change)
        self.proxy = c2

    @staticmethod
    async def date_time_change(self, msg):
        self.parent.value = self.value
        self.parent.date.value = self.value
        await self.parent.proxy.run_method('hide()', msg.websocket)

    @staticmethod
    def input_change(self, msg):
        self.date.value = self.value


def convert_date(date_string):
    date = datetime.datetime.strptime(str(date_string), '%Y-%m-%d')
    return (date - epoch).total_seconds()*1000


async def get_chart(self, msg):
    self.loading = True
    await msg.page.update()
    data = await jp.JustPy.loop.run_in_executor(None, functools.partial(pdr.DataReader, data_source='yahoo', start=self.start_date.value, end=self.end_date.value), self.ticker.value)
    data['Date'] = data.index.astype(str)
    chart = jp.HighStock(a=msg.page, classes='q-ma-md', options=chart_dict, style='height: 600px')
    o = chart.options
    ticker = self.ticker.value
    o.title.text = f'{ticker} Historical Prices'
    x = list(data['Date'].map(convert_date))
    o.series[0].data = list(zip(x, data['Open'], data['High'], data['Low'], data['Close']))
    o.series[0].name = ticker
    o.series[1].data = list(zip(x, data['Volume']))
    self.loading = False


async def stock_test(request):
    wp = jp.QuasarPage(highcharts_theme='grid')
    d = jp.Div(classes="q-ma-md q-gutter-md row", a=wp)
    ticker = jp.QInput(label='Ticker', a=d, value='MSFT')
    start_date = QInputDate(a=d, label='Start Date', standout=True, value='2007-01-01')
    end_date = QInputDate(a=d, label='End Date', standout=True, value='2019-12-31')
    b = jp.QBtn(label='Get Chart', a=d, start_date=start_date, end_date=end_date, ticker=ticker, click=get_chart, loading=False)
    return wp



jp.justpy(stock_test)

```