from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.responses import PlainTextResponse
from starlette.endpoints import WebSocketEndpoint
from starlette.endpoints import HTTPEndpoint
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from justpy.htmlcomponents import *
from .chartcomponents import *
from .gridcomponents import *
from .quasarcomponents import *
from jpcore.template import Context
from jpcore.justpy_app import cookie_signer, JustpyApp,JustpyEndpoint
from jpcore.justpy_config import config, AGGRID, AGGRID_ENTERPRISE,BOKEH,COOKIE_MAX_AGE, CRASH
from jpcore.justpy_config import DEBUG,DECKGL, FAVICON, HIGHCHARTS,HOST,KATEX, LATENCY,LOGGING_LEVEL
from jpcore.justpy_config import MEMORY_DEBUG, NO_INTERNET, PLOTLY, PORT, SECRET_KEY, SESSION_COOKIE_NAME, SESSIONS
from jpcore.justpy_config import SSL_CERTFILE, SSL_KEYFILE, SSL_VERSION, STATIC_DIRECTORY,STATIC_NAME, STATIC_ROUTE
from jpcore.justpy_config import QUASAR, QUASAR_VERSION,TAILWIND, UVICORN_LOGGING_LEVEL, VEGA
JustPy.LOGGING_LEVEL = LOGGING_LEVEL
# from .misccomponents import *
from .meadows import *
from .pandas import *
from .routing import Route, JpRoute, SetRoute
from .utilities import run_task, create_delayed_task
import uvicorn, logging, uuid, sys, os, traceback, fnmatch

current_module = sys.modules[__name__]
current_dir = os.path.dirname(current_module.__file__)
print(current_dir.replace("\\", "/"))
print(f"Module directory: {current_dir}, Application directory: {os.getcwd()}")

TEMPLATES_DIRECTORY = config(
    "TEMPLATES_DIRECTORY", cast=str, default=current_dir + "/templates"
)
#
# globals
#
# uvicorn Server
jp_server = None

def create_component_file_list():
    file_list = []
    component_dir = os.path.join(STATIC_DIRECTORY, "components")
    if os.path.isdir(component_dir):
        for file in os.listdir(component_dir):
            if fnmatch.fnmatch(file, "*.js"):
                file_list.append(f"/components/{file}")
    return file_list


templates = Jinja2Templates(directory=TEMPLATES_DIRECTORY)

component_file_list = create_component_file_list()

template_options = {
    "tailwind": TAILWIND,
    "quasar": QUASAR,
    "quasar_version": QUASAR_VERSION,
    "highcharts": HIGHCHARTS,
    "aggrid": AGGRID,
    "aggrid_enterprise": AGGRID_ENTERPRISE,
    "static_name": STATIC_NAME,
    "component_file_list": component_file_list,
    "no_internet": NO_INTERNET,
    "katex": KATEX,
    "plotly": PLOTLY,
    "bokeh": BOKEH,
    "deckgl": DECKGL,
    "vega": VEGA,
}
logging.basicConfig(level=LOGGING_LEVEL, format="%(levelname)s %(module)s: %(message)s")

# modify middleware handling according to deprecation
# https://github.com/encode/starlette/discussions/1762
middleware = [Middleware(GZipMiddleware)]
if SSL_KEYFILE and SSL_CERTFILE:
    middleware.append(Middleware(HTTPSRedirectMiddleware))
app = JustpyApp(middleware=middleware, debug=DEBUG)
app.mount(STATIC_ROUTE, StaticFiles(directory=STATIC_DIRECTORY), name=STATIC_NAME)
app.mount(
    "/templates", StaticFiles(directory=current_dir + "/templates"), name="templates"
)


def initial_func(_request):
    """
    Default func/endpoint to be called if none has been specified
    """
    wp = WebPage()
    Div(
        text="JustPy says: Page not found",
        classes="inline-block text-5xl m-3 p-3 text-white bg-blue-600",
        a=wp,
    )
    return wp


func_to_run = initial_func
startup_func = None


def server_error_func(request):
    wp = WebPage()
    Div(
        text="JustPy says: 500 - Server Error",
        classes="inline-block text-5xl m-3 p-3 text-white bg-red-600",
        a=wp,
    )
    return wp

@app.on_event("startup")
async def justpy_startup():
    WebPage.loop = asyncio.get_event_loop()
    JustPy.loop = WebPage.loop
    JustPy.STATIC_DIRECTORY = STATIC_DIRECTORY

    if startup_func:
        if inspect.iscoroutinefunction(startup_func):
            await startup_func()
        else:
            startup_func()
    protocol = "https" if SSL_KEYFILE else "http"
    print(f"JustPy ready to go on {protocol}://{HOST}:{PORT}")


@app.route("/{path:path}")
class Homepage(JustpyEndpoint):
    """
    Justpy main page handler
    """
    
    
    def get_response_for_load_page(self,request,load_page):
        """
        get the response for the given webpage
        
        Args:
            request(Request): the request to handle
            load_page(WebPage): the webpage to wrap with justpy and  
            return as a full HtmlResponse
        
        Returns:
            Reponse: the response for the given load_page
        """
        page_type = type(load_page)
        assert issubclass(
            page_type, WebPage
        ), f"Function did not return a web page but a {page_type.__name__}"
        assert (
            len(load_page) > 0 or load_page.html
        ), "\u001b[47;1m\033[93mWeb page is empty, add components\033[0m"
        page_options = {
            "reload_interval": load_page.reload_interval,
            "body_style": load_page.body_style,
            "body_classes": load_page.body_classes,
            "css": load_page.css,
            "head_html": load_page.head_html,
            "body_html": load_page.body_html,
            "display_url": load_page.display_url,
            "dark": load_page.dark,
            "title": load_page.title,
            "redirect": load_page.redirect,
            "highcharts_theme": load_page.highcharts_theme,
            "debug": load_page.debug,
            "events": load_page.events,
            "favicon": load_page.favicon if load_page.favicon else FAVICON,
        }
        if load_page.use_cache:
            page_dict = load_page.cache
        else:
            page_dict = load_page.build_list()
        template_options["tailwind"] = load_page.tailwind
        context = {
            "request": request,
            "page_id": load_page.page_id,
            "justpy_dict": json.dumps(page_dict, default=str),
            "use_websockets": json.dumps(WebPage.use_websockets),
            "options": template_options,
            "page_options": page_options,
            "html": load_page.html,
        }
        # wrap the context in a context object to make it available
        context_obj = Context(context)
        context["context_obj"] = context_obj
        response = templates.TemplateResponse(load_page.template_file, context)
        return response
    
    
        
    async def post(self, request):
        # Handles post method. Used in Ajax mode for events when websockets disabled
        if request["path"] == "/zzz_justpy_ajax":
            data_dict = await request.json()
            # {'type': 'event', 'event_data': {'event_type': 'beforeunload', 'page_id': 0}}
            if data_dict["event_data"]["event_type"] == "beforeunload":
                return await self.on_disconnect(data_dict["event_data"]["page_id"])

            session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
            if SESSIONS and session_cookie:
                session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                data_dict["event_data"]["session_id"] = session_id

            # data_dict['event_data']['session'] = request.session
            msg_type = data_dict["type"]
            data_dict["event_data"]["msg_type"] = msg_type
            page_event = True if msg_type == "page_event" else False
            result = await handle_event(data_dict, com_type=1, page_event=page_event)
            if result:
                if LATENCY:
                    await asyncio.sleep(LATENCY / 1000)
                return JSONResponse(result)
            else:
                return JSONResponse(False)

    async def on_disconnect(self, page_id):
        logging.debug(f"In disconnect Homepage")
        await WebPage.instances[
            page_id
        ].on_disconnect()  # Run the specific page disconnect function
        return JSONResponse(False)


@app.websocket_route("/")
class JustpyEvents(WebSocketEndpoint):

    socket_id = 0

    async def on_connect(self, websocket):
        await websocket.accept()
        websocket.id = JustpyEvents.socket_id
        websocket.open = True
        logging.debug(f"Websocket {JustpyEvents.socket_id} connected")
        JustpyEvents.socket_id += 1
        # Send back socket_id to page
        # await websocket.send_json({'type': 'websocket_update', 'data': websocket.id})
        WebPage.loop.create_task(
            websocket.send_json({"type": "websocket_update", "data": websocket.id})
        )

    async def on_receive(self, websocket, data):
        """
        Method to accept and act on data received from websocket
        """
        logging.debug("%s %s", f"Socket {websocket.id} data received:", data)
        data_dict = json.loads(data)
        msg_type = data_dict["type"]
        # data_dict['event_data']['type'] = msg_type
        if msg_type == "connect":
            # Initial message sent from browser after connection is established
            # WebPage.sockets is a dictionary of dictionaries
            # First dictionary key is page id
            # Second dictionary key is socket id
            page_key = data_dict["page_id"]
            websocket.page_id = page_key
            if page_key in WebPage.sockets:
                WebPage.sockets[page_key][websocket.id] = websocket
            else:
                WebPage.sockets[page_key] = {websocket.id: websocket}
            return
        if msg_type == "event" or msg_type == "page_event":
            # Message sent when an event occurs in the browser
            session_cookie = websocket.cookies.get(SESSION_COOKIE_NAME)
            if SESSIONS and session_cookie:
                session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                data_dict["event_data"]["session_id"] = session_id
            # await self._event(data_dict)
            data_dict["event_data"]["msg_type"] = msg_type
            page_event = True if msg_type == "page_event" else False
            WebPage.loop.create_task(
                handle_event(data_dict, com_type=0, page_event=page_event)
            )
            return
        if msg_type == "zzz_page_event":
            # Message sent when an event occurs in the browser
            session_cookie = websocket.cookies.get(SESSION_COOKIE_NAME)
            if SESSIONS and session_cookie:
                session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                data_dict["event_data"]["session_id"] = session_id
            data_dict["event_data"]["msg_type"] = msg_type
            WebPage.loop.create_task(
                handle_event(data_dict, com_type=0, page_event=True)
            )
            return

    async def on_disconnect(self, websocket, close_code):
        try:
            pid = websocket.page_id
        except:
            return
        websocket.open = False
        WebPage.sockets[pid].pop(websocket.id)
        if not WebPage.sockets[pid]:
            WebPage.sockets.pop(pid)
        await WebPage.instances[pid].on_disconnect(
            websocket
        )  # Run the specific page disconnect function
        if MEMORY_DEBUG:
            print("************************")
            print(
                "Elements: ",
                len(JustpyBaseComponent.instances),
                JustpyBaseComponent.instances,
            )
            print("WebPages: ", len(WebPage.instances), WebPage.instances)
            print("Sockets: ", len(WebPage.sockets), WebPage.sockets)
            import psutil
            process = psutil.Process(os.getpid())
            print(f"Memory used: {process.memory_info().rss:,}")
            print("************************")

async def handle_event(data_dict, com_type=0, page_event=False):
    # com_type 0: websocket, con_type 1: ajax
    connection_type = {0: "websocket", 1: "ajax"}
    logging.info(
        "%s %s %s", "In event handler:", connection_type[com_type], str(data_dict)
    )
    event_data = data_dict["event_data"]
    try:
        p = WebPage.instances[event_data["page_id"]]
    except:
        logging.warning("No page to load")
        return
    event_data["page"] = p
    if com_type == 0:
        event_data["websocket"] = WebPage.sockets[event_data["page_id"]][
            event_data["websocket_id"]
        ]
    # The page_update event is generated by the reload_interval Ajax call
    if event_data["event_type"] == "page_update":
        build_list = p.build_list()
        return {"type": "page_update", "data": build_list}

    if page_event:
        c = p
    else:
        component_id = event_data["id"]
        c = JustpyBaseComponent.instances.get(component_id, None)
        if c is not None:
            event_data["target"] = c
        else:
            logging.warning(
                f"component with id {component_id} doesn't exist (anymore ...) it might have been deleted before the event handling was triggered"
            )

    try:
        if c is not None:
            before_result = await c.run_event_function("before", event_data, True)
    except:
        pass
    try:
        if c is not None:
            if hasattr(c, "on_" + event_data["event_type"]):
                event_result = await c.run_event_function(
                    event_data["event_type"], event_data, True
                )
            else:
                event_result = None
                logging.debug(f"{c} has no {event_data['event_type']} event handler")
        else:
            event_result = None
        logging.debug(f"Event result:{event_result}")
    except Exception as e:
        # raise Exception(e)
        if CRASH:
            print(traceback.format_exc())
            sys.exit(1)
        event_result = None
        # logging.info('%s %s', 'Event result:', '\u001b[47;1m\033[93mAttempting to run event handler:' + str(e) + '\033[0m')
        logging.info(
            "%s %s",
            "Event result:",
            "\u001b[47;1m\033[93mError in event handler:\033[0m",
        )
        logging.info("%s", traceback.format_exc())

    if p.meadows:
        await update_lists(p)
    # If page is not to be updated, the event_function should return anything but None
    if event_result is None:
        if com_type == 0:  # WebSockets communication
            if LATENCY:
                await asyncio.sleep(LATENCY / 1000)
            await p.update()
        elif com_type == 1:  # Ajax communication
            build_list = p.build_list()
    try:
        if c is not None:
            after_result = await c.run_event_function("after", event_data, True)
    except:
        pass
    if com_type == 1 and event_result is None:
        dict_to_send = {
            "type": "page_update",
            "data": build_list,
            "page_options": {
                "display_url": p.display_url,
                "title": p.title,
                "redirect": p.redirect,
                "open": p.open,
                "favicon": p.favicon,
            },
        }
        return dict_to_send


def get_server():
    """
    Workaround for global variable jp_server not working as expected
    """
    return jp_server


def justpy(
    func=None,
    *,
    start_server: bool = True,
    websockets: bool = True,
    host: str = HOST,
    port: int = PORT,
    startup=None,
    init_server: bool = True,
    **kwargs,
):
    """

    The main justpy entry point

    Args:
        func: the callback to get the webpage
        start_server(bool): if True start the server
        websockets(bool): if True use websockets
        host(str): the host to start from e.g. localhost or 0.0.0.0 to listen on all interfaces
        port(int): the port to use for listening
        startup: a callback for the startup phase
        init_server(bool): if True construct the server
        kwargs: further keyword arguments

    """
    global jp_server, func_to_run, startup_func, HOST, PORT

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
    JpRoute("/{path:path}", func_to_run, name="default")
    for k, v in kwargs.items():
        template_options[k.lower()] = v

    if init_server:
        if SSL_KEYFILE and SSL_CERTFILE:
            uvicorn_config = uvicorn.config.Config(
                app,
                host=host,
                port=port,
                log_level=UVICORN_LOGGING_LEVEL,
                proxy_headers=True,
                ssl_keyfile=SSL_KEYFILE,
                ssl_certfile=SSL_CERTFILE,
                ssl_version=SSL_VERSION,
            )
        else:
            uvicorn_config = uvicorn.config.Config(
                app, host=host, port=port, log_level=UVICORN_LOGGING_LEVEL
            )
        jp_server = uvicorn.Server(uvicorn_config)
        if start_server:
            jp_server.run()

    return func_to_run


def convert_dict_to_object(d):
    obj = globals()[d["class_name"]]()
    for obj_prop in d["object_props"]:
        obj.add(convert_dict_to_object(obj_prop))
    # combine the dictionaries
    for k, v in {**d, **d["attrs"]}.items():
        if k != "id":
            obj.__dict__[k] = v
    return obj


def redirect(url):
    wp = WebPage()
    wp.add(Div())
    wp.redirect = url
    return wp
