# Use Decorators for Request Handlers

In this example, the decorator `valid_id` is defined that modifies a request handler to redirect to the home page if the user is not logged in.

This is done using the JustPy function `redirect` that accepts as an argument the URL to redirect to. The function returns a WebPage instance with the `redirect` attribute set based on the parameter.

```python
import justpy as jp
from functools import wraps


logged_in = {}

def test_id(id):
    return id in logged_in

def valid_id(f):
    @wraps(f)
    def wrapper(request):
        bool_outcome = test_id(request.session_id)
        if bool_outcome:
            return f(request)
        else:
            return jp.redirect('/')
    return wrapper


def login_user(self, msg):
    logged_in[msg.session_id] = True


@jp.SetRoute('/login')
def login_page(request):
    wp = jp.WebPage()
    btn = jp.Button(text='Login', classes='m-4 ' + jp.Styles.button_simple, click=login_user, a=wp)
    return wp


@jp.SetRoute('/info')
@valid_id
def info_page(request):
    wp = jp.WebPage()
    jp.Div(text='Some info', classes='m-2 text-xl', a=wp)
    return wp

def home_page():
    wp = jp.WebPage()
    jp.A(text='Click to go to login page ', href='/login', a=wp, classes='m-4 text-xl' )
    return wp


jp.justpy(home_page)


```