import inspect
import asyncio
from types import SimpleNamespace
from addict import Dict


def print_request(request):
    """
    Prints all the request fields
    :param request:
    :return:
    """
    # See https://www.starlette.io/routing/ for path_params
    # and https://github.com/encode/starlette/blob/master/starlette/routing.py line 82
    print(type(request._scope))
    d = dict(request._scope)
    print(d)
    d.pop('headers')
    print(d)
    fields = ['path', 'method', 'url', 'headers', 'query_params', 'path_params', 'client', 'cookies', 'state']
    print('*************************************')
    for field in fields:
        # print(field, request[field])
        try:
            print(field, request[field])
        except:
            print(field, getattr(request, field))
    # print(dir(request.state))
    print(request.url.path, request.url.port, request.url.scheme, dir(request.url))
    for i,j in request.query_params.items():
        print(i,j)
    print('URL stuff -------')
    for j in ['components', 'fragment', 'hostname', 'is_secure', 'netloc', 'password', 'path', 'port', 'query', 'replace', 'scheme', 'username']:
        print(j, getattr(request.url, j))
    for j in (getattr(request.url, 'components')):
        print(j)
    # print(dict(getattr(request.url, 'components')))
    print('*************************************')

async def run_event_function(component, event_type, event_data, create_namespace_flag=False):
    """
    create_namespace converts dictionary so dotted attribute acces is possible

    :param component:
    :param event_type:
    :param event_data:
    :return:
    """
    event_function = getattr(component, 'on_' + event_type)
    if create_namespace_flag:
        function_data = create_namespace(event_data)
    else:
        function_data = event_data
    if inspect.iscoroutinefunction(event_function):
        event_result = await event_function(function_data)
    else:
        event_result = event_function(function_data)
    return event_result


class JustPyRequest:
    pass


async def run_periodically(func, period):
    """
    Run func every period seconds
    :param func: Function to run
    :param period: Period in seconds. Will run
    :return:
    """
    loop = asyncio.get_event_loop()
    while True:
        task1 = loop.create_task(func())
        await asyncio.sleep(period)

def run_task(task):
    loop = asyncio.get_event_loop()
    loop.create_task(task)


async def create_delayed_task(task, delay, loop):
    await asyncio.sleep(delay)
    loop.create_task(task)

# msg = {'event_type': 'submit', 'id': 1, 'class_name': 'Form', 'html_tag': 'form', 'event_target': '1', 'event_current_target': '1', 'running_id': 0, 'page_id': 0, 'form_data': [{'html_tag': 'input', 'id': '2', 'name': 'cat1', 'type': 'radio', 'value': 'volvo', 'class': 'form-radio', 'checked': False}, {'html_tag': 'input', 'id': '4', 'name': 'cat1', 'type': 'radio', 'value': 'volvo 12', 'class': 'form-radio', 'checked': False}, {'html_tag': 'input', 'id': '6', 'name': 'cat1', 'type': 'radio', 'value': 'volvo 13', 'checked': True}, {'html_tag': 'input', 'id': '8', 'name': 'cat1123', 'type': 'checkbox', 'value': 'volvocheck', 'checked': True}, {'html_tag': 'button', 'id': '9', 'value': ''}], 'session_id': '92a895d72fca4443aa9effb0b70f8229', 'page': 'page object'}

def create_namespace(msg):
    j = Dict(msg)
    return j
    j = SimpleNamespace(**msg)
    # if hasattr(j, 'form_data'):
    if j.form_data:
        for counter, value in enumerate(j.form_data):
            j.form_data[counter] = SimpleNamespace(**j.form_data[counter])
    if hasattr(j, 'points'):
        for counter, value in enumerate(j.points):
            j.points[counter] = SimpleNamespace(**j.points[counter])
    return j


# for attr, value in sn.__dict__.items():
#     print(attr, value)

