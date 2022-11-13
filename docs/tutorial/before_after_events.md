# The "before" and "after" Events
[The "before" and "after" Events live demo]({{demo_url}}/after_demo)

Occasionally, you need to do something before an event handler is run, or after the event handler is run.

For example, before the input event handler is run, you would like the value of the Python element to reflect the value of the respective input element on the page. Even if you have not assigned an input handler to that particular element, you may want to update the value anyway so it is available for other event handlers or background tasks.

In fact, this is what happens with Input and QInput elements. Even when they are not assigned an input event handler, they run an event handler for the <span style="color: red">before</span> event to correctly update the value of the element.

In the example below, a different notification is shown for each button clicked. This is done by setting the `show` attribute of the notification to `True` in the click event handler. Then, the <span style="color: red">after</span> event handler is run, and it sets the `show` attribute back to `False` so that it is not displayed next time the page is updated.

JustPy updates the page after an event handler for any event that is not <span style="color: red">before</span> or <span style="color: red">after</span> is run (unless the event handler does not return `None`). JustPy does **not** update the page after the <span style="color: red">before</span> and <span style="color: red">after</span> event handlers.

Try running the example below as is and then without binding an <span style="color: red">after</span> event handler to the buttons and see what happens.

```python
import justpy as jp

btn_classes = jp.Styles.button_outline + ' m-2'
notification_classes = 'm-2 text-center text-xl bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded w-64'


def btn_click(self, msg):
    self.nl[self.list_index].show = True


def btn_after(self, msg):
    self.nl[self.list_index].show = False


def after_demo():
    wp = jp.WebPage()
    btn_list = []
    notification_list = []

    for index, btn_text in enumerate(['First', 'Second', 'Third']):
        btn_list.append(jp.Button(text=f'{btn_text} Button', classes=btn_classes, a=wp,
                                  nl=notification_list, list_index=index,
                                  click=btn_click, after=btn_after))

    for notification_text in ['First', 'Second', 'Third']:
        notification_list.append(jp.Div(text=f'{notification_text} Notification',
                                        classes=notification_classes, a=wp, show=False))

    return wp


jp.justpy(after_demo)

```
