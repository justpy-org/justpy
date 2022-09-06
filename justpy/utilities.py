import asyncio
import inspect


def print_request(request):
    # See https://www.starlette.io/routing/ for path_params
    # and https://github.com/encode/starlette/blob/master/starlette/routing.py line 82
    print(type(request._scope))
    d = dict(request._scope)
    print(d)
    d.pop("headers")
    print(d)
    fields = [
        "path",
        "method",
        "url",
        "headers",
        "query_params",
        "path_params",
        "client",
        "cookies",
        "state",
    ]
    print("*************************************")
    for field in fields:
        # print(field, request[field])
        try:
            print(field, request[field])
        except:
            print(field, getattr(request, field))
    print(request.url.path, request.url.port, request.url.scheme, dir(request.url))
    for i, j in request.query_params.items():
        print(i, j)
    print("URL related -------")
    for j in [
        "components",
        "fragment",
        "hostname",
        "is_secure",
        "netloc",
        "password",
        "path",
        "port",
        "query",
        "replace",
        "scheme",
        "username",
    ]:
        print(j, getattr(request.url, j))
    for j in getattr(request.url, "components"):
        print(j)
    print("*************************************")


def run_task(task):
    """
    Helper function to facilitate running a task in the async loop
    """
    loop = asyncio.get_event_loop()
    loop.create_task(task)


async def create_delayed_task(task, delay, loop):
    await asyncio.sleep(delay)
    loop.create_task(task)


def print_func_info(*args):
    # Calling function name
    print(inspect.stack()[1][3])
    for i in args:
        print(i)
