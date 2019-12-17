import psutil, gc
MEMORY_DEBUG = True
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse
from starlette.endpoints import WebSocketEndpoint
from starlette.endpoints import HTTPEndpoint
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.config import Config
# from starlette.routing import Router, Mount
# from starlette.datastructures import CommaSeparatedStrings, Secret
from itsdangerous import Signer
import typing
# from .htmlcomponents import *
from .chartcomponents import *
from .gridcomponents import *
from .quasarcomponents import *
from .pandas import *
from .routing import Route, SetRoute
from .utilities import run_task, create_delayed_task, print_request
import uvicorn, logging, uuid, sys, os
from ssl import PROTOCOL_SSLv23
#TODO: https://github.com/kennethreitz/setup.py setup.py file https://github.com/pypa/sampleproject/blob/master/setup.py
#TODO: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-18-04-server

current_module = sys.modules[__name__]
current_dir = os.path.dirname(current_module.__file__)

config = Config('justpy.env')
DEBUG = config('DEBUG', cast=bool, default=True)
LATENCY = config('LATENCY', cast=int, default=0)
if LATENCY:
    print(f'Simulating latency of {LATENCY} ms')
SESSIONS = config('SESSIONS', cast=bool, default=True)
SESSION_COOKIE_NAME = config('SESSION_COOKIE_NAME', cast=str, default='jp_token')
SECRET_KEY = config('SECRET_KEY', default='$$$my_secret_string$$$')    # Make sure to change when deployed
LOGGING_LEVEL = config('LOGGING_LEVEL', default=logging.WARNING)
JustPy.LOGGING_LEVEL = LOGGING_LEVEL
UVICORN_LOGGING_LEVEL = config('UVICORN_LOGGING_LEVEL', default='WARNING').lower()
COOKIE_MAX_AGE = config('COOKIE_MAX_AGE', cast=int, default=60*60*24*7)   # One week in seconds
HOST = config('HOST', cast=str, default='0.0.0.0')
PORT = config('PORT', cast=int, default=8000)
SSL_VERSION = config('SSL_VERSION', default=PROTOCOL_SSLv23)
SSL_KEYFILE = config('SSL_KEYFILE', default='')
SSL_CERTFILE = config('SSL_CERTFILE', default='')

TEMPLATES_DIRECTORY = config('TEMPLATES_DIRECTORY', cast=str, default=current_dir + '/templates')
# STATIC_DIRECTORY = config('STATIC_DIRECTORY', cast=str, default=current_dir + '/static')
STATIC_DIRECTORY = config('STATIC_DIRECTORY', cast=str, default=os.getcwd())
STATIC_ROUTE = config('STATIC_MOUNT', cast=str, default='/static')
STATIC_NAME = config('STATIC_NAME', cast=str, default='static')
print(current_dir, os.getcwd())
FAVICON = config('FAVICON', cast=str, default='')  # If False gets value from https://elimintz.github.io/favicon.png
TAILWIND = config('TAILWIND', cast=bool, default=True)
QUASAR = config('QUASAR', cast=bool, default=False)
HIGHCHARTS = config('HIGHCHARTS', cast=bool, default=True)
AGGRID = config('AGGRID', cast=bool, default=True)

template_options = {'tailwind': TAILWIND, 'quasar': QUASAR, 'highcharts': HIGHCHARTS, 'aggrid': AGGRID,
                    'static_name': STATIC_NAME}
logging.basicConfig(level=LOGGING_LEVEL, format='%(levelname)s %(module)s: %(message)s')

templates = Jinja2Templates(directory=TEMPLATES_DIRECTORY)

app = Starlette(debug=DEBUG)
app.mount(STATIC_ROUTE, StaticFiles(directory=STATIC_DIRECTORY), name=STATIC_NAME)

app.add_middleware(GZipMiddleware, minimum_size=1000)
if SSL_KEYFILE and SSL_CERTFILE:
    app.add_middleware(HTTPSRedirectMiddleware)


def initial_func(request):
    wp = WebPage()
    Div(text='JustPy says: Page not found', classes='inline-block text-5xl m-3 p-3 text-white bg-blue-600', a=wp)
    return wp

func_to_run = initial_func
startup_func = None

cookie_signer = Signer(str(SECRET_KEY))

@app.on_event('startup')
async def justpy_startup():
    WebPage.loop = asyncio.get_event_loop()
    JustPy.loop = WebPage.loop
    if startup_func:
        if inspect.iscoroutinefunction(startup_func):
            await startup_func()
        else:
            startup_func()
    print(f'JustPy ready to go on http://127.0.0.1:{PORT} or http://localhost:{PORT}')


@app.route("/{path:path}")
class Homepage(HTTPEndpoint):


    async def get(self, request):
        session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
        if SESSIONS:
            new_cookie = False
            if session_cookie:
                try:
                    session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                except:
                    return PlainTextResponse('Bad Session')
                request.state.session_id = session_id
                request.session_id = session_id
            else:
                # Create new session_id
                request.state.session_id = str(uuid.uuid4().hex)
                request.session_id = request.state.session_id
                new_cookie = True
                logging.debug(f'New session_id created: {request.session_id}')
        for route in Route.instances:
            func = route.matches(request['path'], request)
            if func:
                func_to_run = func
                break
        func_parameters = len(inspect.signature(func_to_run).parameters)
        assert func_parameters < 2, f"Function {func_to_run.__name__} cannot have more than one parameter"
        if inspect.iscoroutinefunction(func_to_run):
            if func_parameters == 1:
                load_page = await func_to_run(request)
            else:
                load_page = await func_to_run()
        else:
            if func_parameters == 1:
                load_page = func_to_run(request)
            else:
                load_page = func_to_run()
        assert issubclass(type(load_page), WebPage), 'Function did not return a web page'
        page_options = {'reload_interval': load_page.reload_interval, 'body_style': load_page.body_style,
                        'body_classes': load_page.body_classes, 'css': load_page.css, 'scripts': load_page.head_html,
                        'display_url': load_page.display_url, 'dark': load_page.dark, 'title': load_page.title,
                        'highcharts_theme': load_page.highcharts_theme,
                        'favicon': load_page.favicon if load_page.favicon else FAVICON}
        if load_page.use_cache:
            page_dict = load_page.cache
        else:
            page_dict = load_page.build_list()
        context = {'request': request, 'page_id': load_page.page_id, 'justpy_dict': json.dumps(page_dict),
                   'use_websockets': json.dumps(WebPage.use_websockets), 'options': template_options, 'page_options': page_options,
                   'html': load_page.html}
        # response = templates.TemplateResponse('tailwind.html', context)
        response = templates.TemplateResponse(load_page.template_file, context)
        if SESSIONS and new_cookie:
            cookie_value = cookie_signer.sign(request.state.session_id)
            cookie_value = cookie_value.decode("utf-8")
            response.set_cookie(SESSION_COOKIE_NAME, cookie_value, max_age=COOKIE_MAX_AGE, httponly=True)
        if LATENCY:
            await asyncio.sleep(LATENCY/1000)
        return response


    async def post(self, request):
        # Handles post method. Used in Ajax mode for events when websockets disabled
        if request['path']=='/zzz_justpy_ajax':
            data_dict = await request.json()
            # {'type': 'event', 'event_data': {'event_type': 'beforeunload', 'page_id': 0}}
            if data_dict['event_data']['event_type']== 'beforeunload':
                return await self.on_disconnect(data_dict['event_data']['page_id'])

            # if data_dict['type']=='initial':
            #     return JSONResponse('')
            session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
            if session_cookie:
                session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                data_dict['event_data']['session_id'] = session_id

            # data_dict['event_data']['session'] = request.session
            result = await handle_event(data_dict, com_type=1)
            if result:
                if LATENCY:
                    await asyncio.sleep(LATENCY / 1000)
                return JSONResponse(result)
            else:
                return JSONResponse(False)

    async def on_disconnect(self, page_id):
        logging.debug(f'In disconnect Homepage')
        await WebPage.instances[page_id].on_disconnect()  # Run the specific page disconnect function
        logging.debug(WebPage.instances)
        return JSONResponse(False)

@app.websocket_route("/")
class JustpyEvents(WebSocketEndpoint):

    socket_id = 0

    async def on_connect(self, websocket):
        await websocket.accept()
        websocket.id = JustpyEvents.socket_id
        websocket.open = True
        logging.debug(f'Websocket {str(JustpyEvents.socket_id)} connected')
        JustpyEvents.socket_id += 1
        #Send back socket_id for the tooltip event
        await websocket.send_json({'type': 'websocket_update', 'data': websocket.id})

    async def on_receive(self, websocket, data):
        """
        Routine to accept and act on data received from websocket
        :param websocket:
        :param data: Data sent through websocket
        :return:
        """

        logging.debug('%s %s',f'Socket {str(websocket.id)} data received:', data)
        data_dict = json.loads(data)
        msg_type = data_dict['type']
        if msg_type == 'connect':
            # Initial message sent from browser after connection is established
            await self._connect(websocket, data_dict)
            return
        if msg_type == 'event':
            # Message sent when an event occurs in the browser
            # data_dict['event_data']['session'] = websocket.session
            session_cookie = websocket.cookies.get(SESSION_COOKIE_NAME)
            if session_cookie:
                session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                data_dict['event_data']['session_id'] = session_id
            await self._event(data_dict)
            return


    async def on_disconnect(self, websocket, close_code):
        pid = websocket.page_id
        websocket.open = False
        WebPage.sockets[pid].pop(websocket.id)
        if not WebPage.sockets[pid]:
            WebPage.sockets.pop(pid)
        await WebPage.instances[pid].on_disconnect(websocket)   # Run the specific page disconnect function
        if MEMORY_DEBUG:
            print('************************')
            print(len(JustpyBaseComponent.instances),JustpyBaseComponent.instances)
            print(WebPage.instances)
            print(len(WebPage.sockets), WebPage.sockets)
            # gc.collect()
            process = psutil.Process(os.getpid())
            print(f'Memory used: {process.memory_info().rss:,}')
            print('************************')


    async def _connect(self, websocket, data_dict):
        # WebPage.sockets is a dictionary of dictionaries
        # First dictionary key is page id
        # Second dictionary key is socket id
        page_key = data_dict['page_id']
        websocket.page_id = page_key
        if page_key in WebPage.sockets:
            WebPage.sockets[page_key][websocket.id] = websocket
        else:
            WebPage.sockets[page_key] = {websocket.id: websocket}


    async def _event(self, data_dict):
        # com_type 0: websocket, com_type 1: ajax
        await handle_event(data_dict, com_type=0)
        return




async def handle_event(data_dict, com_type=0):
    # com_type 0: websocket, con_type 1: ajax
    connection_type = {0: 'websocket', 1: 'ajax'}
    logging.info('%s %s %s', 'In event handler:', connection_type[com_type], str(data_dict))
    event_data = data_dict['event_data']
    try:
        p = WebPage.instances[event_data['page_id']]
    except:
        logging.warning('No page to load')
        return
    event_data['page'] = p
    if com_type==0:
        event_data['websocket'] = WebPage.sockets[event_data['page_id']][event_data['websocket_id']]
    if event_data['event_type'] == 'page_update':
        #TODO: Add event handler for page_update (add events to WebPage)
        build_list = p.build_list()
        return {'type': 'page_update', 'data': build_list}
    c = JustpyBaseComponent.instances[event_data['id']]
    try:
        # before_result = await run_event_function(c, 'before', event_data, True)
        before_result = await c.run_event_function('before', event_data, True)
    except:
        pass
    try:
        # event_result = await run_event_function(c, event_data['event_type'], event_data, True)
        event_result = await c.run_event_function(event_data['event_type'], event_data, True)
        logging.debug('%s %s', 'Event result:', event_result)
    except Exception as e:
        # raise Exception(e)
        event_result = None
        logging.info('%s %s', 'Event result:', '\u001b[47;1m\033[93mAttempting to run event handler:' + str(e) + '\033[0m')

    # If page is not to be updated, the event_function should return anything but None

    if event_result is None:
        if com_type == 0:     # WebSockets communication
            if LATENCY:
                await asyncio.sleep(LATENCY / 1000)
            await p.update()
        elif com_type == 1:   # Ajax communication
            build_list = p.build_list()
    try:
        # after_result = await run_event_function(c, 'after', event_data, True)
        after_result = await c.run_event_function('after', event_data, True)
    except:
        pass
    if com_type == 1 and event_result is None:
        return {'type': 'page_update', 'data': build_list}


def justpy(func=None, start_server=True, websockets=True, host=HOST, port=PORT, startup=None, **kwargs):
    global func_to_run, startup_func
    if func:
        func_to_run = func
    else:
        func_to_run = initial_func
    if startup:
        startup_func = startup
    if websockets:
        WebPage.use_websockets = True
    else:
        WebPage.use_websockets = False
    Route("/{path:path}", func_to_run, last=True, name='default')
    for k, v in kwargs.items():
        template_options[k.lower()] = v

    # host = '0.0.0.0'
    if start_server:
        if SSL_KEYFILE and SSL_CERTFILE:
            uvicorn.run(app, host=host, port=port, log_level=UVICORN_LOGGING_LEVEL, proxy_headers=True,
                        ssl_keyfile=SSL_KEYFILE, ssl_certfile=SSL_CERTFILE, ssl_version=SSL_VERSION)
        else:
            uvicorn.run(app, host=host, port=port, log_level=UVICORN_LOGGING_LEVEL)

    return func_to_run

def convert_dict_to_object(d):
    obj = globals()[d['class_name']](temp=True)
    for obj_prop in d['object_props']:
        obj.add(convert_dict_to_object(obj_prop))
    for k,v in d.items():
        obj.__dict__[k] = v
    return obj



