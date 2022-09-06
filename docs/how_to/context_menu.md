# Addiing a Context Menu (right-click in browser)


```python
import justpy as jp


def my_click(self, msg):
    print(msg)
    self.text = f'Mouse button clicked: {msg.which}'
    # Show context menu div and place it near the click
    if msg.which == 3:
        msg.page.context_menu.remove_class('hidden')
        msg.page.context_menu.style = f'top{msg.pageY}px; left: {msg.pageX}px;'


def click_out(self, msg):
    self.set_class('hidden')


def context_event_demo():
    wp = jp.WebPage()
    wp.head_html = """
    <script>
    window.oncontextmenu = function () {
      return false;     // cancel default menu
    }
    </script>
    """
    d = jp.Div(text='Not clicked yet', a=wp, classes='w-64 text-xl m-2 p-1 bg-blue-500 text-white')
    d.add_event('mousedown')
    d.on('mousedown', my_click)
    d.additional_properties =['screenX', 'pageY', 'pageX', 'altKey', 'which', 'movementX',' button', 'buttons']
    # In your case you would build a more elaborate div
    wp.context_menu = jp.Div(text='My context menu', classes='hidden absolute border text-white bg-blue-500', a=wp)
    wp.context_menu.on('click__out', click_out)
    return wp


jp.justpy(context_event_demo)
```

The JavaScript added to the page disables the default behavior of the context menu. Then, you use the mousedown event to detect which button was pressed. In order to do this we modify the element to add additional fields to msg from the JavaScript event.

click__out is also used to hide the simple context menu when there is a click outside of it.
