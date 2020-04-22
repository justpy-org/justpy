from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse
from starlette.endpoints import WebSocketEndpoint
from starlette.endpoints import HTTPEndpoint
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.config import Config
from itsdangerous import Signer
from .htmlcomponents import *
from .chartcomponents import *
from .gridcomponents import *
from .quasarcomponents import *
from .pandas import *
from .routing import Route, SetRoute
from .utilities import run_task, create_delayed_task
import uvicorn, logging, uuid, sys, os, traceback, fnmatch
from ssl import PROTOCOL_SSLv23

current_module = sys.modules[__name__]
current_dir = os.path.dirname(current_module.__file__)
print(current_dir.replace('\\', '/'))
print(f'Module directory: {current_dir}, Application directory: {os.getcwd()}')

config = Config('justpy.env')
DEBUG = config('DEBUG', cast=bool, default=True)
MEMORY_DEBUG = config('MEMORY_DEBUG', cast=bool, default=False)
if MEMORY_DEBUG:
    import psutil
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
HOST = config('HOST', cast=str, default='127.0.0.1')
PORT = config('PORT', cast=int, default=8000)
SSL_VERSION = config('SSL_VERSION', default=PROTOCOL_SSLv23)
SSL_KEYFILE = config('SSL_KEYFILE', default='')
SSL_CERTFILE = config('SSL_CERTFILE', default='')

TEMPLATES_DIRECTORY = config('TEMPLATES_DIRECTORY', cast=str, default=current_dir + '/templates')
STATIC_DIRECTORY = config('STATIC_DIRECTORY', cast=str, default=os.getcwd())
STATIC_ROUTE = config('STATIC_MOUNT', cast=str, default='/static')
STATIC_NAME = config('STATIC_NAME', cast=str, default='static')
FAVICON = config('FAVICON', cast=str, default='')  # If False gets value from https://elimintz.github.io/favicon.png
TAILWIND = config('TAILWIND', cast=bool, default=True)
QUASAR = config('QUASAR', cast=bool, default=False)
HIGHCHARTS = config('HIGHCHARTS', cast=bool, default=True)
AGGRID = config('AGGRID', cast=bool, default=True)
AGGRID_ENTERPRISE = config('AGGRID_ENTERPRISE', cast=bool, default=False)

NO_INTERNET = config('NO_INTERNET', cast=bool, default=False)

def create_component_file_list():
    file_list = []
    component_dir = f'{STATIC_DIRECTORY}\\components'
    if os.path.isdir(component_dir):
        for file in os.listdir(component_dir):
            if fnmatch.fnmatch(file, '*.js'):
                file_list.append(f'/components/{file}')
    return file_list


templates = Jinja2Templates(directory=TEMPLATES_DIRECTORY)

component_file_list = create_component_file_list()

template_options = {'tailwind': TAILWIND, 'quasar': QUASAR, 'highcharts': HIGHCHARTS, 'aggrid': AGGRID, 'aggrid_enterprise': AGGRID_ENTERPRISE,
                    'static_name': STATIC_NAME, 'component_file_list': component_file_list, 'no_internet': NO_INTERNET}
logging.basicConfig(level=LOGGING_LEVEL, format='%(levelname)s %(module)s: %(message)s')


app = Starlette(debug=DEBUG)
app.mount(STATIC_ROUTE, StaticFiles(directory=STATIC_DIRECTORY), name=STATIC_NAME)
app.mount('/templates', StaticFiles(directory=current_dir + '/templates'), name='templates')
app.add_middleware(GZipMiddleware)
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
    print(f'JustPy ready to go on http://{HOST}:{PORT}')


@app.route("/{path:path}")

class Homepage(HTTPEndpoint):

    async def get(self, request):
        # Handle web requests
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
        assert len(load_page) > 0 or load_page.html, '\u001b[47;1m\033[93mWeb page is empty, add components\033[0m'
        page_options = {'reload_interval': load_page.reload_interval, 'body_style': load_page.body_style,
                        'body_classes': load_page.body_classes, 'css': load_page.css, 'head_html': load_page.head_html, 'body_html': load_page.body_html,
                        'display_url': load_page.display_url, 'dark': load_page.dark, 'title': load_page.title,
                        'highcharts_theme': load_page.highcharts_theme, 'debug': load_page.debug, 'events': load_page.events,
                        'favicon': load_page.favicon if load_page.favicon else FAVICON}
        if load_page.use_cache:
            page_dict = load_page.cache
        else:
            page_dict = load_page.build_list()
        template_options['tailwind'] = load_page.tailwind
        context = {'request': request, 'page_id': load_page.page_id, 'justpy_dict': json.dumps(page_dict, default=str),
                   'use_websockets': json.dumps(WebPage.use_websockets), 'options': template_options, 'page_options': page_options,
                   'html': load_page.html}
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
            if data_dict['event_data']['event_type'] == 'beforeunload':
                return await self.on_disconnect(data_dict['event_data']['page_id'])

            session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
            if SESSIONS and session_cookie:
                session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                data_dict['event_data']['session_id'] = session_id

            # data_dict['event_data']['session'] = request.session
            msg_type = data_dict['type']
            data_dict['event_data']['msg_type'] = msg_type
            page_event = True if msg_type == 'page_event' else False
            result = await handle_event(data_dict, com_type=1, page_event=page_event)
            if result:
                if LATENCY:
                    await asyncio.sleep(LATENCY / 1000)
                return JSONResponse(result)
            else:
                return JSONResponse(False)

    async def on_disconnect(self, page_id):
        logging.debug(f'In disconnect Homepage')
        await WebPage.instances[page_id].on_disconnect()  # Run the specific page disconnect function
        return JSONResponse(False)


@app.websocket_route("/")
class JustpyEvents(WebSocketEndpoint):

    socket_id = 0

    async def on_connect(self, websocket):
        await websocket.accept()
        websocket.id = JustpyEvents.socket_id
        websocket.open = True
        logging.debug(f'Websocket {JustpyEvents.socket_id} connected')
        JustpyEvents.socket_id += 1
        #Send back socket_id to page
        # await websocket.send_json({'type': 'websocket_update', 'data': websocket.id})
        WebPage.loop.create_task(websocket.send_json({'type': 'websocket_update', 'data': websocket.id}))

    async def on_receive(self, websocket, data):
        """
        Method to accept and act on data received from websocket
        """
        logging.debug('%s %s',f'Socket {websocket.id} data received:', data)
        data_dict = json.loads(data)
        msg_type = data_dict['type']
        # data_dict['event_data']['type'] = msg_type
        if msg_type == 'connect':
            # Initial message sent from browser after connection is established
            # WebPage.sockets is a dictionary of dictionaries
            # First dictionary key is page id
            # Second dictionary key is socket id
            page_key = data_dict['page_id']
            websocket.page_id = page_key
            if page_key in WebPage.sockets:
                WebPage.sockets[page_key][websocket.id] = websocket
            else:
                WebPage.sockets[page_key] = {websocket.id: websocket}
            return
        if msg_type == 'event' or msg_type == 'page_event':
            # Message sent when an event occurs in the browser
            session_cookie = websocket.cookies.get(SESSION_COOKIE_NAME)
            if SESSIONS and session_cookie:
                session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                data_dict['event_data']['session_id'] = session_id
            # await self._event(data_dict)
            data_dict['event_data']['msg_type'] = msg_type
            page_event = True if msg_type == 'page_event' else False
            WebPage.loop.create_task(handle_event(data_dict, com_type=0, page_event=page_event))
            return
        if msg_type == 'zzz_page_event':
            # Message sent when an event occurs in the browser
            session_cookie = websocket.cookies.get(SESSION_COOKIE_NAME)
            if SESSIONS and session_cookie:
                session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                data_dict['event_data']['session_id'] = session_id
            data_dict['event_data']['msg_type'] = msg_type
            WebPage.loop.create_task(handle_event(data_dict, com_type=0, page_event=True))
            return

    async def on_disconnect(self, websocket, close_code):
        pid = websocket.page_id
        websocket.open = False
        WebPage.sockets[pid].pop(websocket.id)
        if not WebPage.sockets[pid]:
            WebPage.sockets.pop(pid)
        await WebPage.instances[pid].on_disconnect(websocket)   # Run the specific page disconnect function
        # WebPage.loop.create_task(WebPage.instances[pid].on_disconnect(websocket))
        if MEMORY_DEBUG:
            print('************************')
            print('Elements: ', len(JustpyBaseComponent.instances), JustpyBaseComponent.instances)
            print('WebPages: ', len(WebPage.instances), WebPage.instances)
            print('Sockets: ', len(WebPage.sockets), WebPage.sockets)
            process = psutil.Process(os.getpid())
            print(f'Memory used: {process.memory_info().rss:,}')
            print('************************')



async def handle_event(data_dict, com_type=0, page_event=False):
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
    # The page_update event is generated by the reload_interval Ajax call
    if event_data['event_type'] == 'page_update':
        build_list = p.build_list()
        return {'type': 'page_update', 'data': build_list}

    if page_event:
        c = p
    else:
        c = JustpyBaseComponent.instances[event_data['id']]

    try:
        before_result = await c.run_event_function('before', event_data, True)
    except:
        pass
    try:
        event_result = await c.run_event_function(event_data['event_type'], event_data, True)
        logging.debug('%s %s', 'Event result:', event_result)
    except Exception as e:
        # raise Exception(e)
        event_result = None
        # logging.info('%s %s', 'Event result:', '\u001b[47;1m\033[93mAttempting to run event handler:' + str(e) + '\033[0m')
        logging.info('%s %s', 'Event result:', '\u001b[47;1m\033[93mAttempting to run event handler:\033[0m')
        logging.debug('%s', traceback.format_exc())

    # If page is not to be updated, the event_function should return anything but None

    if event_result is None:
        if com_type == 0:     # WebSockets communication
            if LATENCY:
                await asyncio.sleep(LATENCY / 1000)
            await p.update()
        elif com_type == 1:   # Ajax communication
            build_list = p.build_list()
    try:
        after_result = await c.run_event_function('after', event_data, True)
    except:
        pass
    if com_type == 1 and event_result is None:
        dict_to_send = {'type': 'page_update', 'data': build_list,
                        'page_options': {'display_url': p.display_url,
                                         'title': p.title,
                                         'redirect': p.redirect, 'open': p.open,
                                         'favicon': p.favicon}}
        return dict_to_send


def justpy(func=None, *, start_server=True, websockets=True, host=HOST, port=PORT, startup=None, **kwargs):
    global func_to_run, startup_func, HOST, PORT
    HOST = host
    PORT = port
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

    if start_server:
        if SSL_KEYFILE and SSL_CERTFILE:
            uvicorn.run(app, host=host, port=port, log_level=UVICORN_LOGGING_LEVEL, proxy_headers=True,
                        ssl_keyfile=SSL_KEYFILE, ssl_certfile=SSL_CERTFILE, ssl_version=SSL_VERSION)
        else:
            uvicorn.run(app, host=host, port=port, log_level=UVICORN_LOGGING_LEVEL)

    return func_to_run


def convert_dict_to_object(d):
    obj = globals()[d['class_name']]()
    for obj_prop in d['object_props']:
        obj.add(convert_dict_to_object(obj_prop))
    # combine the dictionaries
    for k,v in {**d, **d['attrs']}.items():
        if k != 'id':
            obj.__dict__[k] = v
    return obj


