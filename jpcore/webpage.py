'''
Created on 2022-09-12

@author: wf
'''
from addict import Dict
import asyncio
import inspect
from types import MethodType

class WebPage:
    """
    a web page
    """ 
    # TODO: Add page events online, beforeunload, resize
    instances = {}
    sockets = {}
    next_page_id = 0
    use_websockets = True
    delete_flag = True
    tailwind = True
    debug = False
    highcharts_theme = None
    # One of ['avocado', 'dark-blue', 'dark-green', 'dark-unica', 'gray',
    # 'grid-light', 'grid', 'high-contrast-dark', 'high-contrast-light', 'sand-signika', 'skies', 'sunset']
    allowed_events = [
        "click",
        "visibilitychange",
        "page_ready",
        "result_ready",
        "keydown",
        "keyup",
        "keypress",
    ]

    def __init__(self, **kwargs):
        self.page_id = WebPage.next_page_id
        WebPage.next_page_id += 1
        self.cache = None  # Set this attribute if you want to use the cache.
        self.use_cache = False  # Determines whether the page uses the cache or not
        self.template_file = "tailwind.html"
        self.title = "JustPy"
        self.display_url = None
        self.redirect = None
        self.open = None
        self.favicon = None
        self.components = []  # list of direct children components on page
        self.cookies = {}
        self.css = ""
        self.head_html = ""
        self.body_html = ""
        # If html attribute is not empty, sets html of page directly
        self.html = ""
        self.body_style = ""
        self.body_classes = ""
        self.reload_interval = None
        self.events = []
        self.dark = (
            False  # Set to True for Quasar dark mode (use for other dark modes also)
        )
        self.data = {}
        WebPage.instances[self.page_id] = self
        for k, v in kwargs.items():
            self.__setattr__(k, v)
            
    def __repr__(self):
        return f"{self.__class__.__name__}(page_id: {self.page_id}, number of components: {len(self.components)}, reload interval: {self.reload_interval})"

    def __len__(self):
        return len(self.components)

    def add_component(self, child, position=None):
        if position is None:
            self.components.append(child)
        else:
            self.components.insert(position, child)
        return self

    async def on_disconnect(self, websocket=None):
        if self.delete_flag:
            self.delete_components()
            self.remove_page()

    def remove_page(self):
        WebPage.instances.pop(self.page_id)

    def delete_components(self):
        for c in self.components:
            c.delete()
        self.components = []

    def add(self, *args):
        for component in args:
            self.add_component(component)
        return self

    def __add__(self, other):
        self.add_component(other)
        return self

    def __iadd__(self, other):
        self.add_component(other)
        return self

    def remove_component(self, component):
        try:
            self.components.remove(component)
        except:
            raise Exception("Component cannot be removed because it was not in Webpage")
        return self

    def remove(self, component):
        self.remove_component(component)

    def get_components(self):
        return self.components

    def last(self):
        return self.components[-1]

    def set_cookie(self, k, v):
        self.cookies[str(k)] = str(v)

    def delete_cookie(self, k):
        if k in self.cookies:
            del self.cookies[str(k)]

    async def run_javascript(self, javascript_string, *, request_id=None, send=True):
        try:
            websocket_dict = WebPage.sockets[self.page_id]
        except:
            return self
        dict_to_send = {
            "type": "run_javascript",
            "data": javascript_string,
            "request_id": request_id,
            "send": send,
        }
        await asyncio.gather(
            *[
                websocket.send_json(dict_to_send)
                for websocket in list(websocket_dict.values())
            ],
            return_exceptions=True,
        )
        return self

    async def reload(self):
        return await self.run_javascript("location.reload()")

    async def update_old(self, *, built_list=None):
        try:
            websocket_dict = WebPage.sockets[self.page_id]
        except:
            return self
        if not built_list:
            component_build = self.build_list()
        else:
            component_build = built_list
        for websocket in list(websocket_dict.values()):
            try:
                WebPage.loop.create_task(
                    websocket.send_json(
                        {
                            "type": "page_update",
                            "data": component_build,
                            "page_options": {
                                "display_url": self.display_url,
                                "title": self.title,
                                "redirect": self.redirect,
                                "open": self.open,
                                "favicon": self.favicon,
                            },
                        }
                    )
                )
            except:
                print("Problem with websocket in page update, ignoring")
        return self

    async def update(self, websocket=None):
        """
        update the Webpage

        Args:
            websocket(): The websocket to use (if any)
        """
        try:
            websocket_dict = WebPage.sockets[self.page_id]
        except:
            return self
        page_build = self.build_list()
        dict_to_send = {
            "type": "page_update",
            "data": page_build,
            "page_options": {
                "display_url": self.display_url,
                "title": self.title,
                "redirect": self.redirect,
                "open": self.open,
                "favicon": self.favicon,
            },
        }

        if websocket:
            WebPage.loop.create_task(websocket.send_json(dict_to_send))
        else:
            websockets = list(websocket_dict.values())
            # https://stackoverflow.com/questions/54987361/python-asyncio-handling-exceptions-in-gather-documentation-unclear
            _results = await asyncio.gather(
                *[websocket.send_json(dict_to_send) for websocket in websockets],
                return_exceptions=True,
            )
            pass
        return self

    async def delayed_update(self, delay):
        await asyncio.sleep(delay)
        return await self.update()

    def to_html(self, indent=0, indent_step=0, format=True):
        block_indent = " " * indent
        if format:
            ws = "\n"
        else:
            ws = ""
        s = f"{block_indent}<div>{ws}"
        for c in self.components:
            s = f"{s}{c.to_html(indent + indent_step, indent_step, format)}"
        s = f"{s}{block_indent}</div>{ws}"
        return s

    def react(self):
        pass

    def build_list(self):
        object_list = []
        self.react()
        for i, obj in enumerate(self.components):
            obj.react(self.data)
            d = obj.convert_object_to_dict()
            object_list.append(d)
        return object_list

    def on(self, event_type, func):
        """
        add an event of the given event_type  with the given function
        
        Args:
            event_type(str): the type of the event without on_prefix
            func(Callable): the function to call
            
        """
        if event_type in self.allowed_events:
            if inspect.ismethod(func):
                setattr(self, "on_" + event_type, func)
            else:
                setattr(self, "on_" + event_type, MethodType(func, self))
            if event_type not in self.events:
                self.events.append(event_type)
        else:
            raise Exception(f"No event of type {event_type} supported")

    async def run_event_function(
        self, event_type, event_data, create_namespace_flag=True
    ):
        event_function = getattr(self, "on_" + event_type)
        if create_namespace_flag:
            function_data = Dict(event_data)
        else:
            function_data = event_data
        if inspect.iscoroutinefunction(event_function):
            event_result = await event_function(function_data)
        else:
            event_result = event_function(function_data)
        return event_result

    def add_event(self, event):
        if event not in self.allowed_events:
            self.allowed_events.append(event)