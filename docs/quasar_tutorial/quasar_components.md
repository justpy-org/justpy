# QAjaxBar


```python
import justpy as jp

async def start_bar(self, msg):
    wp = msg.page
    await wp.ajax_bar.run_method('start()', msg.websocket)

async def stop_bar(self, msg):
    wp = msg.page
    await wp.ajax_bar.run_method('stop()', msg.websocket)


def ajax_bar_example():
    wp = jp.QuasarPage()
    d = jp.Div(classes='q-pa-md', a=wp)
    # temp=False is important because this generates an id for the element that is required for run_method to work
    wp.ajax_bar = jp.QAjaxBar(position='bottom', color='accent', size='10px', skip_hijack=True, a=d, temp=False)
    btn_start = jp.QBtn(color='primary', label='Start Bar', a=d, click=start_bar, style='margin-right: 20px')
    btn_stop = jp.QBtn(color='primary', label='Stop Bar', a=d, click=stop_bar)
    return wp

jp.justpy(ajax_bar_example)

```

# QBtnToggle

[QBtnToggle component](https://quasar.dev/vue-components/button-toggle) is similar to a radio group but with buttons.

```python
import justpy as jp

# Example from https://www.highcharts.com/docs/getting-started/your-first-chart
my_chart_def = """
{
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Chart of Type Bar'
        },
        xAxis: {
            categories: ['Apples', 'Bananas', 'Oranges']
        },
        yAxis: {
            title: {
                text: 'Fruit eaten'
            }
        },
        series: [{
            name: 'Jane',
            data: [1, 0, 4]
        }, {
            name: 'John',
            data: [5, 7, 3]
        }]
}
"""

def button_change(self, msg):
    print(msg)
    self.chart.options.chart.type = self.value
    self.chart.options.title.text = f'Chart of Type {self.value}'

def button_toggle_test():
    wp = jp.QuasarPage()
    chart_type = jp.QBtnToggle(toggle_color='red', push=True, glossy=True, a=wp, input=button_change, value='bar', classes='q-ma-md')
    for type in ['bar', 'column', 'line', 'spline']:
        chart_type.options.append({'label': type.capitalize(), 'value': type})
    chart_type.chart = jp.HighCharts(a=wp, classes='q-ma-lg', options=my_chart_def)
    return wp


jp.justpy(button_toggle_test)
```