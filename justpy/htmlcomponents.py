from types import MethodType
from addict import Dict
import json, copy, inspect, sys, re
from html.parser import HTMLParser, tagfind_tolerant, attrfind_tolerant
from html.entities import name2codepoint
from html import unescape
from jinja2 import Template
import asyncio
from jpcore.tailwind import Tailwind
import logging
import httpx
from jpcore.template import PageOptions
from jpcore.component import Component
from jpcore.webpage import WebPage as BaseWebPage

# Dictionary for translating from tag to class
_tag_class_dict = {}


def parse_dict(cls):
    """
    Decorator for component class definitions that updates _tag_class_dict so that the parser can recognize new components
    Required only for components not defined in this module
    """
    _tag_class_dict[cls.html_tag] = cls
    return cls


class JustPy:
    loop = None
    LOGGING_LEVEL = logging.DEBUG
    component_registry = {}
    
class WebPage(BaseWebPage):
    """
    enhanced WebPage as per documentation
    """
    
    def write(self, md_text):
        """
        write to a Markdown div
        """
        assert _has_markdown, "Markdown not installed"
        return Markdown(
            markdown=md_text, a=self, classes="m-2 p-2", all_extensions=True
        )

    def equation(self, eq_text):
        """
        return an Equation linked to this webpage with the given equation text
        """
        return Equation(equation=eq_text, a=self, classes="m-2 p-2")

def register_component(component_class, tag, attributes=[]):
    JustPy.component_registry[tag] = {
        "class": component_class,
        "attributes": attributes,
    }


class Register:
    def __init__(self, tag, attributes=[], **kwargs):
        self.tag = tag
        self.kwargs = kwargs
        self.attributes = attributes

    def __call__(self, cls, **kwargs):
        register_component(cls, self.tag, self.attributes)
        return cls

class TailwindVersion1Page(WebPage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tailwind = False
        self.head_html = """
        <link rel="stylesheet" href="https://unpkg.com/tailwindcss@^1.5/dist/base.min.css" />
        <link rel="stylesheet" href="https://unpkg.com/tailwindcss@^1.5/dist/components.min.css" />
        <link rel="stylesheet" href="https://unpkg.com/@tailwindcss/typography@0.2.x/dist/typography.min.css"/>
        <link rel="stylesheet" href="https://unpkg.com/tailwindcss@^1.5/dist/utilities.min.css" />
        """

class TailwindUIPage(WebPage):
    # https://tailwindui.com/components

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_file = "tailwindui.html"

class JustpyBaseComponent(Component):
    """
    the base class for all Justpy components
    """
    temp_flag = True
    delete_flag = True
    needs_deletion = False

    def __init__(self, **kwargs):
        """
        constructor
        """
        cls = JustpyBaseComponent
        temp = kwargs.get("temp", cls.temp_flag)
        delete_flag = kwargs.get("delete_flag", cls.delete_flag)
        if temp and delete_flag:
            self.id = None
        else:
            self.id = cls.next_id
            cls.next_id += 1
        self.events = []
        self.event_modifiers = Dict()
        self.transition = None
        self.allowed_events = []

    def initialize(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        self.set_keyword_events(**kwargs)
        for com in ["a", "add_to"]:
            if com in kwargs.keys():
                kwargs[com].add_component(self)

    def set_keyword_events(self, **kwargs):
        for e in self.allowed_events:
            for prefix in ["", "on", "on_"]:
                if prefix + e in kwargs.keys():
                    cls = JustpyBaseComponent
                    if not self.id:
                        self.id = cls.next_id
                        cls.next_id += 1
                    fn = kwargs[prefix + e]
                    if isinstance(fn, str):
                        fn_string = f"def oneliner{self.id}(self, msg):\n {fn}"
                        exec(fn_string)
                        self.on(e, locals()[f"oneliner{self.id}"])
                    else:
                        self.on(e, fn)
                    break

    def delete(self):
        if self.needs_deletion:
            if self.delete_flag:
                JustpyBaseComponent.instances.pop(self.id, None)
                self.needs_deletion = False

    def on(
        self,
        event_type,
        func,
        *,
        debounce=None,
        throttle=None,
        immediate=False,
    ):
        if event_type in self.allowed_events:
            cls = JustpyBaseComponent
            if not self.id:
                self.id = cls.next_id
                cls.next_id += 1
            cls.instances[self.id] = self
            self.needs_deletion = True
            if inspect.ismethod(func):
                setattr(self, "on_" + event_type, func)
            else:
                setattr(self, "on_" + event_type, MethodType(func, self))
            if event_type not in self.events:
                self.events.append(event_type)
            if debounce:
                self.event_modifiers[event_type].debounce = {
                    "value": debounce,
                    "timeout": None,
                    "immediate": immediate,
                }
            elif throttle:
                self.event_modifiers[event_type].throttle = {
                    "value": throttle,
                    "timeout": None,
                }
        else:
            raise Exception(f"No event of type {event_type} supported")

    def remove_event(self, event_type):
        if event_type in self.events:
            self.events.remove(event_type)

    def has_event_function(self, event_type):
        if getattr(self, "on_" + event_type, None):
            return True
        else:
            return False

    def has_class(self, class_name):
        return class_name in self.classes.split()

    def remove_class(self, tw_class):
        class_list = self.classes.split()
        try:
            class_list.remove(tw_class)
        except:
            pass
        self.classes = " ".join(class_list)

    def hidden(self, flag=True):
        if flag:
            self.set_class("hidden")
        else:
            self.remove_class("hidden")

    def hidden_toggle(self):
        if self.has_class("hidden"):
            self.remove_class("hidden")
        else:
            self.set_class("hidden")

    async def update(self, socket=None, *, react=None):
        if react:
            self.react([])
        component_dict = self.convert_object_to_dict()
        if socket:
            await socket.send_json({"type": "component_update", "data": component_dict})
        else:
            pages_to_update = list(self.pages.values())
            for page in pages_to_update:
                try:
                    websocket_dict = WebPage.sockets[page.page_id]
                except:
                    continue
                for websocket in list(websocket_dict.values()):
                    try:
                        # WebPage.loop.create_task(websocket.send_json({'type': 'component_update', 'data': component_dict}))
                        await websocket.send_json(
                            {"type": "component_update", "data": component_dict}
                        )
                    except:
                        print("Problem with websocket in component update, ignoring")
        return self

    def check_transition(self):
        if self.transition and (not self.id):
            cls = JustpyBaseComponent
            self.id = cls.next_id
            cls.next_id += 1

    async def run_method(self, command, websocket):
        await websocket.send_json(
            {"type": "run_method", "data": command, "id": self.id}
        )
        # So the page itself does not update, return True not None
        return True

    def remove_page_from_pages(self, wp: WebPage):
        self.pages.pop(wp.page_id)

    def add_page(self, wp: WebPage):
        self.pages[wp.page_id] = wp

    def add_page_to_pages(self, wp: WebPage):
        self.pages[wp.page_id] = wp

    def set_model(self, value):
        if hasattr(self, "model"):
            if len(self.model) == 2:
                self.model[0].data[self.model[1]] = value
            else:
                self.model[0][self.model[1]] = value

    def get_model(self):
        if len(self.model) == 2:
            model_value = self.model[0].data[self.model[1]]
        else:
            model_value = self.model[0][self.model[1]]
        return model_value

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

    @staticmethod
    def convert_dict_to_object(d):
        obj = globals()[d["class_name"]]()
        for obj_prop in d["object_props"]:
            obj.add(JustpyBaseComponent.convert_dict_to_object(obj_prop))
        for k, v in d.items():
            obj.__dict__[k] = v
        for k, v in d["attrs"].items():
            obj.__dict__[k] = v
        return obj


class HTMLBaseComponent(JustpyBaseComponent):
    """
    Base Component for all HTML components
    """

    attributes = []
    html_tag = "div"
    vue_type = "html_component"  # Vue.js component name

    html_global_attributes = [
        "accesskey",
        "class",
        "contenteditable",
        "dir",
        "draggable",
        "dropzone",
        "hidden",
        "id",
        "lang",
        "spellcheck",
        "style",
        "tabindex",
        "title",
    ]

    attribute_list = [
        "id",
        "vue_type",
        "show",
        "events",
        "event_modifiers",
        "classes",
        "style",
        "set_focus",
        "html_tag",
        "class_name",
        "event_propagation",
        "inner_html",
        "animation",
        "debug",
        "transition",
    ]

    # not_used_global_attributes = ['dropzone', 'translate', 'autocapitalize',
    #                               'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype']

    # Additions to global attributes to add to attrs dict apart from id and style.
    used_global_attributes = [
        "contenteditable",
        "dir",
        "tabindex",
        "title",
        "accesskey",
        "draggable",
        "lang",
        "spellcheck",
    ]

    # https://developer.mozilla.org/en-US/docs/Web/HTML/Element

    # windows_events = ['afterprint', 'beforeprint', 'beforeunload', 'error', 'hashchange', 'load',
    #                   'message', 'offline', 'online', 'pagehide', 'pageshow', 'popstate',
    #                   'resize', 'storage', 'unload']
    # form_events = ['blur', 'change', 'contextmenu', 'focus', 'input', 'invalid', 'reset', 'search', 'select', 'submit']
    # keyboard_events = ['keydown', 'keypress', 'keyup']
    # mouse_events = ['click', 'dblclick', 'mousedown', 'mousemove', 'mouseout', 'mouseover', 'mouseup', 'wheel',
    #                 'mouseenter', 'mouseleave']
    # allowed_events = ['click', 'mouseover', 'mouseout', 'mouseenter', 'mouseleave', 'input', 'change',
    #                   'after', 'before', 'keydown', 'keyup', 'keypress', 'focus', 'blur']

    # allowed_events = ['click', 'mouseover', 'mouseout', 'mouseenter', 'mouseleave', 'input', 'change',
    #                   'after', 'before', 'keydown', 'keyup', 'keypress', 'focus', 'blur', 'submit',
    #                   'dragstart', 'dragover', 'drop']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.class_name = type(self).__name__
        self.debug = False
        self.inner_html = ""
        self.animation = False
        self.pages = (
            {}
        )  # Dictionary of pages the component is on. Not managed by framework.
        self.show = True
        self.set_focus = False
        self.classes = ""
        self.slot = None
        self.scoped_slots = {}  # For Quasar and other Vue.js based components
        self.style = ""
        self.directives = []
        self.data = {}
        self.drag_options = None
        self.allowed_events = [
            "click",
            "mouseover",
            "mouseout",
            "mouseenter",
            "mouseleave",
            "input",
            "change",
            "after",
            "before",
            "keydown",
            "keyup",
            "keypress",
            "focus",
            "blur",
            "submit",
            "dragstart",
            "dragover",
            "drop",
            "click__out",
        ]
        self.events = []
        self.event_modifiers = Dict()
        self.additional_properties = (
            []
        )  # Additional fields to get from the JavasScript event object
        self.event_propagation = True  # If True events are propagated
        self.prop_list = []  # For components from libraries like quasar

        self.initialize(**kwargs)

    def __len__(self):
        if hasattr(self, "components"):
            return len(self.components)
        else:
            return 0

    def __repr__(self):
        name = self.name if hasattr(self, "name") else "No name"
        return f"{self.__class__.__name__}(id: {self.id}, html_tag: {self.html_tag}, vue_type: {self.vue_type}, name: {name}, number of components: {len(self)})"

    def add_to_page(self, wp: WebPage):
        wp.add_component(self)

    def add_to(self, *args):
        for c in args:
            c.add_component(self)

    def add_attribute(self, attr, value):
        self.attrs[attr] = value

    def add_event(self, event_type):
        if event_type not in self.allowed_events:
            self.allowed_events.append(event_type)

    def add_allowed_event(self, event_type):
        self.add_event(event_type)

    def add_scoped_slot(self, slot, c):
        self.scoped_slots[slot] = c

    def to_html(self, indent=0, indent_step=0, format=True):
        block_indent = " " * indent
        if format:
            ws = "\n"
        else:
            ws = ""
        s = f"{block_indent}<{self.html_tag} "
        d = self.convert_object_to_dict()
        for attr, value in d["attrs"].items():
            if value:
                s = f'{s}{attr}="{value}" '
        if self.classes:
            s = f'{s}class="{self.classes}"/>{ws}'
        else:
            s = f"{s}/>{ws}"
        return s

    def react(self, data):
        return

    def convert_object_to_dict(self):
        d = {}
        # Add id if CSS transition is defined
        if self.transition:
            self.check_transition()
        if self.id:
            d["attrs"] = {"id": str(self.id)}
        else:
            d["attrs"] = {}
        for attr in HTMLBaseComponent.attribute_list:
            d[attr] = getattr(self, attr)
        d["directives"] = {}
        for i in self.directives:
            if i[0:2] == "v-":  # It is a directive
                try:
                    d["directives"][i[2:]] = getattr(self, i.replace("-", "_"))
                except:
                    pass
        for i in (
            self.prop_list + self.attributes + HTMLBaseComponent.used_global_attributes
        ):
            try:
                d["attrs"][i] = getattr(self, i)
            except:
                pass
            if i in ["in", "from"]:  # Attributes that are also python reserved words
                try:
                    d["attrs"][i] = getattr(self, "_" + i)
                except:
                    pass
            if "-" in i:
                s = i.replace("-", "_")  # kebab case to snake case
                try:
                    d["attrs"][i] = getattr(self, s)
                except:
                    pass
        # Name is a special case. Allow it to be defined for all
        try:
            d["attrs"]["name"] = self.name
        except:
            pass
        d["scoped_slots"] = {}
        for s in self.scoped_slots:
            d["scoped_slots"][s] = self.scoped_slots[s].convert_object_to_dict()
        if self.additional_properties:
            d["additional_properties"] = self.additional_properties
        if self.drag_options:
            d["drag_options"] = self.drag_options
        return d


class Div(HTMLBaseComponent):
    # A general purpose container
    # This is a component that other components can be added to

    html_tag = "div"

    def __init__(self, **kwargs):
        self.html_entity = False
        self.children = []
        super().__init__(**kwargs)
        self.components = self.children.copy()

    def delete(self):
        if self.delete_flag:
            for c in self.components:
                c.delete()
            if self.needs_deletion:
                JustpyBaseComponent.instances.pop(self.id, None)
            self.components = []

    def __getitem__(self, index):
        return self.components[index]

    def add_component(self, child, position=None, slot=None):
        if slot:
            child.slot = slot
        if position is None:
            self.components.append(child)
        else:
            self.components.insert(position, child)
        return self

    def delete_components(self):
        for c in self.components:
            c.delete()
        self.components = []

    def add(self, *args):
        for component in args:
            self.add_component(component)
        return self

    def __add__(self, child):
        self.add_component(child)
        return self

    def __iadd__(self, child):
        self.add_component(child)
        return self

    def add_first(self, child):
        self.add_component(child, 0)

    def remove_component(self, component):
        try:
            self.components.remove(component)
        except:
            raise Exception(
                "Component cannot be removed because it is not contained in element"
            )
        return self

    def remove(self, component):
        self.remove_component(component)

    def get_components(self):
        return self.components

    def first(self):
        return self.components[0]

    def last(self):
        return self.components[-1]

    def to_html(self, indent=0, indent_step=0, format=True):
        block_indent = " " * indent
        if format:
            ws = "\n"
        else:
            ws = ""
        s = f"{block_indent}<{self.html_tag} "
        d = self.convert_object_to_dict()
        for attr, value in d["attrs"].items():
            if value:
                s = f'{s}{attr}="{value}" '
        if self.style:
            s = f'{s}style="{self.style}"'
        if self.classes:
            s = f'{s}class="{self.classes}">{ws}'
        else:
            s = f"{s}>{ws}"
        if self.inner_html:
            s = f"{s}{self.inner_html}</{self.html_tag}>{ws}"
            return s
        try:
            s = f"{s}{self.text}{ws}"
        except:
            pass
        for c in self.components:
            s = f"{s}{c.to_html(indent + indent_step, indent_step, format)}"
        s = f"{s}{block_indent}</{self.html_tag}>{ws}"
        return s

    def model_update(self):
        # [wp, 'text'] for example
        # self.text = str(self.model[0].data[self.model[1]])
        self.text = self.get_model()

    def build_list(self):
        object_list = []
        for i, obj in enumerate(self.components):
            obj.react(self.data)
            d = obj.convert_object_to_dict()
            object_list.append(d)
        return object_list

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        if hasattr(self, "model"):
            self.model_update()
        d["object_props"] = self.build_list()
        if hasattr(self, "text"):
            self.text = str(self.text)
            d["text"] = self.text
            # Handle HTML entities. Warning: They should be in their own span or div. Setting inner_html overrides all else in container
            if self.html_entity:
                d["inner_html"] = self.text
        return d


class Input(Div):
    # Edge and Internet explorer do not support the input event for checkboxes and radio buttons. Use change instead
    # IMPORTANT: Scope of name of radio buttons is the whole page and not the form unless form is specified

    html_tag = "input"
    attributes = [
        "accept",
        "alt",
        "autocomplete",
        "autofocus",
        "checked",
        "dirname",
        "disabled",
        "form",
        "formaction",
        "formenctype",
        "formmethod",
        "formnovalidate",
        "formtarget",
        "height",
        "list",
        "max",
        "maxlength",
        "min",
        "minlength",
        "multiple",
        "name",
        "pattern",
        "placeholder",
        "readonly",
        "required",
        "size",
        "src",
        "step",
        "type",
        "value",
        "width",
    ]

    def __init__(self, **kwargs):

        self.value = ""
        self.checked = False
        self.debounce = 200  # 200 millisecond default debounce for events
        self.no_events = False
        # Types for input element:
        # ['button', 'checkbox', 'color', 'date', 'datetime-local', 'email', 'file', 'hidden', 'image',
        # 'month', 'number', 'password', 'radio', 'range', 'reset', 'search', 'submit', 'tel', 'text', 'time', 'url', 'week']
        self.type = "text"
        self.form = None
        super().__init__(**kwargs)

        def default_input(self, msg):
            return self.before_event_handler(msg)

        if not self.no_events:
            self.on("before", default_input)

    def __repr__(self):
        num_components = len(self.components)
        return f"{self.__class__.__name__}(id: {self.id}, html_tag: {self.html_tag}, input_type: {self.type}, vue_type: {self.vue_type}, value: {self.value}, checked: {self.checked}, number of components: {num_components})"

    def before_event_handler(self, msg):
        logging.debug(
            "%s %s %s %s %s", "before ", self.type, msg.event_type, msg.input_type, msg
        )
        if msg.event_type not in ["input", "change", "select"]:
            return
        if msg.input_type == "checkbox":
            # The checked field is boolean
            self.checked = msg.checked
            if hasattr(self, "model"):
                self.model[0].data[self.model[1]] = msg.checked
        elif msg.input_type == "radio":
            # If a radio field, all other radio buttons with same name need to have value changed
            # If form is specified, the scope is that form. If not, it is the whole page
            self.checked = True
            if self.form:
                Input.radio_button_set(self, self.form)
            else:
                Input.radio_button_set(self, msg.page)
            if hasattr(self, "model"):
                self.model[0].data[self.model[1]] = msg.value
            self.value = msg.value
        else:
            if msg.input_type == "number":
                try:
                    msg.value = int(msg.value)
                except:
                    msg.value = float(msg.value)
            if hasattr(self, "model"):
                # self.model[0].data[self.model[1]] = msg.value
                self.set_model(msg.value)
            self.value = msg.value

    @staticmethod
    def radio_button_set(radio_button, container):
        # Set all radio buttons in container with same name as radio_button to unchecked
        if hasattr(container, "components"):
            for c in container.components:
                if hasattr(c, "name"):
                    if c.name == radio_button.name and not radio_button.id == c.id:
                        c.checked = False
                Input.radio_button_set(radio_button, c)

    @staticmethod
    def radio_button_set_model_update(radio_button, container, model_value):
        for c in container.components:
            if hasattr(c, "name"):
                if c.name == radio_button.name:
                    if c.value == model_value:
                        c.checked = True
                    else:
                        c.checked = False
            Input.radio_button_set_model_update(radio_button, c, model_value)

    def model_update(self):
        # update_value = self.model[0].data[self.model[1]]
        update_value = self.get_model()
        if self.type == "checkbox":
            self.checked = update_value
        elif self.type == "radio":
            model_value = update_value
            if self.form:
                Input.radio_button_set_model_update(self, self.form, model_value)
            else:
                Input.radio_button_set_model_update(self, self.model[0], model_value)
        else:
            self.value = update_value

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["debounce"] = self.debounce
        d[
            "input_type"
        ] = self.type  # Needed for vue component updated life hook and event handler
        if self.type in ["text", "textarea"]:
            d["value"] = str(self.value)
        else:
            d["value"] = self.value
        d["attrs"]["value"] = self.value
        d["checked"] = self.checked
        if not self.no_events:
            if self.type in ["radio", "checkbox", "select"] or self.type == "file":
                # Not all browsers create input event
                if "change" not in self.events:
                    self.events.append("change")
            else:
                if "input" not in self.events:
                    self.events.append("input")
        if self.checked:
            d["attrs"]["checked"] = True
        else:
            d["attrs"]["checked"] = False
        try:
            d["attrs"]["form"] = self.form.id
        except:
            pass

        return d


class InputChangeOnly(Input):
    """
    Does not generate the 'input' event. Generates the 'change' event. Leaves other events unchanged.
    Use if you don't need to look at each character typed. Saves interaction with the server
    The 'change' event docs:
    https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/change_event
    Salient: When the element loses focus after its value was changed, but not committed (e.g., after editing the value
    of <textarea> or <input type="text">) or when Enter is pressed.
    """

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["events"].remove("input")
        if "change" not in d["events"]:
            d["events"].append("change")
        return d


class Form(Div):

    html_tag = "form"
    attributes = [
        "accept-charset",
        "action",
        "autocomplete",
        "enctype",
        "method",
        "name",
        "novalidate",
        "target",
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        def default_submit(self, msg):
            print("Default form submit", msg.form_data)
            return True

        if not self.has_event_function("submit"):
            # If an event handler is not  assigned, the front end cannot stop the default page request that happens when a form is submitted
            self.on("submit", default_submit)


class Label(Div):

    html_tag = "label"
    attributes = [
        "for",
        "form",
    ]  # In JustPy these are components, not ids of component like in HTML

    def __init__(self, **kwargs):
        self.for_component = None
        super().__init__(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        try:
            d["attrs"]["for"] = self.for_component.id
        except:
            pass
        try:
            d["attrs"]["form"] = self.form.id
        except:
            pass
        return d


class Textarea(Input):

    html_tag = "textarea"
    attributes = [
        "autofocus",
        "cols",
        "dirname",
        "disabled",
        "form",
        "maxlength",
        "name",
        "placeholder",
        "readonly",
        "required",
        "rows",
        "wrap",
        "value",
    ]

    def __init__(self, **kwargs):
        self.rows = "4"
        self.cols = "50"
        super().__init__(**kwargs)
        self.type = "textarea"
        self.input_type = "text"


class Select(Input):
    # Need to set value of select on creation, otherwise blank line will show on page update
    html_tag = "select"
    attributes = [
        "autofocus",
        "disabled",
        "form",
        "multiple",
        "name",
        "required",
        "size",
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "select"


class A(Div):

    html_tag = "a"
    attributes = [
        "download",
        "href",
        "hreflang",
        "media",
        "ping",
        "rel",
        "target",
        "type",
    ]

    def __init__(self, **kwargs):

        self.href = None
        self.bookmark = None  # The component on page to jump to or scroll to
        self.title = ""
        self.rel = "noopener noreferrer"
        self.download = None  # If attribute is set, file is downloaded, only works html 5  https://www.w3schools.com/tags/att_a_download.asp
        self.target = "_self"  # _blank, _self, _parent, _top, framename
        # https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView
        self.scroll = False  # If True, scrolling is enabled
        self.scroll_option = "smooth"  # One of "auto" or "smooth".
        self.block_option = "start"  # One of "start", "center", "end", or "nearest". Defaults to "start".
        self.inline_option = "nearest"  # One of "start", "center", "end", or "nearest". Defaults to "nearest".
        super().__init__(**kwargs)

        if not kwargs.get("click"):

            def default_click(self, msg):
                return True

            self.on("click", default_click)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["scroll"] = self.scroll
        d["scroll_option"] = self.scroll_option
        d["block_option"] = self.block_option
        d["inline_option"] = self.inline_option
        if self.bookmark is not None:
            self.href = "#" + str(self.bookmark.id)
            self.scroll_to = str(self.bookmark.id)
        if d["scroll"]:
            d["scroll_to"] = self.scroll_to
        d["attrs"]["href"] = self.href
        d["attrs"]["target"] = self.target
        if self.download is not None:
            d["attrs"]["download"] = self.download
        return d


Link = A  # The 'Link' name is more descriptive and can be used instead


class Icon(Div):
    def __init__(self, **kwargs):
        self.icon = "dog"  # Default icon
        super().__init__(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["classes"] = self.classes + " fa fa-" + self.icon
        return d


class EditorMD(Textarea):
    # https://www.cssportal.com/style-input-range/   style an input range
    # Set the page's tailwind attribute to False for preview to work
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debounce = 0
        self.input_type = "textarea"
        self.vue_type = "editorjp"
        self.html_tag = "textarea"


class Space(Div):

    # Creates a span with hard spaces.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num = kwargs.get("num", 1)
        self.html_tag = "span"
        self.inner_html = "&nbsp;" * self.num


# Non html components


class TabGroup(Div):
    """
    Displays a tab based on its value. Has a dict of tabs whose keys is the value. A tab is any JustPy component.

    format of dict: {'value1': {'tab': comp1, 'order': number}, 'value2': {'tab': comp2, 'order': number} ...}
    self.tabs - tab dict
    self.animation_next = 'slideInRight'    set animation for tab coming in
    self.animation_prev = 'slideOutLeft'    set animation for tab going out
    self.animation_speed = 'faster'  can be on of  '' | 'slow' | 'slower' | 'fast'  | 'faster'
    self.value  value of group and tab to display
    self.previous - previous tab, no need to change except to set to '' in order to display tab without animation which is default at first

    """

    wrapper_classes = " "
    wrapper_style = "display: flex; position: absolute; width: 100%; height: 100%;  align-items: center; justify-content: center; background-color: #fff;"

    def __init__(self, **kwargs):

        self.tabs = (
            {}
        )  # Dict with format 'value': {'tab': Div component, 'order': number} for each entry
        self.value = ""
        self.previous_value = ""
        # https://github.com/daneden/animate.css
        self.animation_next = "slideInRight"
        self.animation_prev = "slideOutLeft"
        self.animation_speed = "faster"  # '' | 'slow' | 'slower' | 'fast'  | 'faster'

        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        if key == "value":
            try:
                self.previous_value = self.value
            except:
                pass
        self.__dict__[key] = value

    def model_update(self):
        self.value = self.model[0].data[self.model[1]]

    def convert_object_to_dict(self):
        self.components = []
        self.wrapper_div_classes = (
            self.animation_speed
        )  # Component in this will be centered

        if self.previous_value:
            self.wrapper_div = Div(
                classes=self.wrapper_div_classes,
                animation=self.animation_next,
                temp=True,
                style=f"{self.__class__.wrapper_style} z-index: 50;",
                a=self,
            )
            self.wrapper_div.add(self.tabs[self.value]["tab"])
            self.wrapper_div = Div(
                classes=self.wrapper_div_classes,
                animation=self.animation_prev,
                temp=True,
                style=f"{self.__class__.wrapper_style} z-index: 0;",
                a=self,
            )
            self.wrapper_div.add(self.tabs[self.previous_value]["tab"])
        else:
            self.wrapper_div = Div(
                classes=self.wrapper_div_classes,
                temp=True,
                a=self,
                style=self.__class__.wrapper_style,
            )
            self.wrapper_div.add(self.tabs[self.value]["tab"])

        self.style = (
            " position: relative; overflow: hidden; " + self.style
        )  # overflow: hidden;
        d = super().convert_object_to_dict()
        return d


# HTML tags for which corresponding classes will be created
_tag_create_list = [
    "address",
    "article",
    "aside",
    "footer",
    "header",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "main",
    "nav",
    "section",
    "blockquote",
    "dd",
    "dl",
    "dt",
    "figcaption",
    "figure",
    "hr",
    "li",
    "ol",
    "p",
    "pre",
    "ul",
    "abbr",
    "b",
    "bdi",
    "bdo",
    "br",
    "cite",
    "code",
    "data",
    "dfn",
    "em",
    "i",
    "kbd",
    "mark",
    "q",
    "rb",
    "rp",
    "rt",
    "rtc",
    "ruby",
    "s",
    "samp",
    "small",
    "span",
    "strong",
    "sub",
    "sup",
    "time",
    "tt",
    "u",
    "var",
    "wbr",
    "area",
    "audio",
    "img",
    "map",
    "track",
    "video",
    "embed",
    "iframe",
    "object",
    "param",
    "picture",
    "source",
    "del",
    "ins",
    "title",
    "caption",
    "col",
    "colgroup",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "tr",
    "button",
    "fieldset",
    "legend",
    "meter",
    "optgroup",
    "option",
    "progress",  # datalist not supported
    "details",
    "summary",
    "style",  # dialog not supported
]

# Only tags that have non-gloabal  attributes that are supported by HTML 5 are in this dict
_attr_dict = {
    "a": ["download", "href", "hreflang", "media", "ping", "rel", "target", "type"],
    "area": [
        "alt",
        "coords",
        "download",
        "href",
        "hreflang",
        "media",
        "rel",
        "shape",
        "target",
        "type",
    ],
    "audio": ["autoplay", "controls", "loop", "muted", "preload", "src"],
    "base": ["href", "target"],
    "bdo": ["dir"],
    "blockquote": ["cite"],
    "button": [
        "autofocus",
        "disabled",
        "form",
        "formaction",
        "formenctype",
        "formmethod",
        "formnovalidate",
        "formtarget",
        "name",
        "type",
        "value",
    ],
    "canvas": ["height", "width"],
    "col": ["span"],
    "colgroup": ["span"],
    "data": ["value"],
    "del": ["cite", "datetime"],
    "details": ["open"],
    "dialog": ["open"],
    "embed": ["height", "src", "type", "width"],
    "fieldset": ["disabled", "form", "name"],
    "form": [
        "accept-charset",
        "action",
        "autocomplete",
        "enctype",
        "method",
        "name",
        "novalidate",
        "target",
    ],
    "html": ["xmlns"],
    "iframe": ["height", "name", "sandbox", "src", "srcdoc", "width"],
    "img": [
        "alt",
        "crossorigin",
        "height",
        "ismap",
        "longdesc",
        "sizes",
        "src",
        "srcset",
        "usemap",
        "width",
    ],
    "input": [
        "accept",
        "alt",
        "autocomplete",
        "autofocus",
        "checked",
        "dirname",
        "disabled",
        "form",
        "formaction",
        "formenctype",
        "formmethod",
        "formnovalidate",
        "formtarget",
        "height",
        "list",
        "max",
        "maxlength",
        "min",
        "minlength",
        "multiple",
        "name",
        "pattern",
        "placeholder",
        "readonly",
        "required",
        "size",
        "src",
        "step",
        "type",
        "value",
        "width",
    ],
    "ins": ["cite", "datetime"],
    "label": ["for", "form"],
    "li": ["value"],
    "link": ["crossorigin", "href", "hreflang", "media", "rel", "sizes", "type"],
    "map": ["name"],
    "meta": ["charset", "content", "http-equiv", "name"],
    "meter": ["form", "high", "low", "max", "min", "optimum", "value"],
    "object": ["data", "form", "height", "name", "type", "usemap", "width"],
    "ol": ["reversed", "start", "type"],
    "optgroup": ["disabled", "label"],
    "option": ["disabled", "label", "selected", "value"],
    "output": ["for", "form", "name"],
    "param": ["name", "value"],
    "progress": ["max", "value"],
    "q": ["cite"],
    "script": ["async", "charset", "defer", "src", "type"],
    "select": ["autofocus", "disabled", "form", "multiple", "name", "required", "size"],
    "source": ["src", "srcset", "media", "sizes", "type"],
    "style": ["media", "type"],
    "td": ["colspan", "headers", "rowspan"],
    "textarea": [
        "autofocus",
        "cols",
        "dirname",
        "disabled",
        "form",
        "maxlength",
        "name",
        "placeholder",
        "readonly",
        "required",
        "rows",
        "wrap",
    ],
    "th": ["abbr", "colspan", "headers", "rowspan", "scope", "sorted"],
    "time": ["datetime"],
    "track": ["default", "kind", "label", "src", "srclang"],
    "video": [
        "autoplay",
        "controls",
        "height",
        "loop",
        "muted",
        "poster",
        "preload",
        "src",
        "width",
    ],
}

# Name definition for static syntax analysers
# Classes are defined dynamically right after, this is just to assist code editors

Address = (
    Article
) = (
    Aside
) = (
    Footer
) = (
    Header
) = (
    H1
) = (
    H2
) = (
    H3
) = (
    H4
) = (
    H5
) = (
    H6
) = (
    Main
) = (
    Nav
) = (
    Section
) = (
    Blockquote
) = (
    Dd
) = (
    Dl
) = (
    Dt
) = (
    Figcaption
) = (
    Figure
) = (
    Hr
) = (
    Li
) = (
    Ol
) = (
    P
) = (
    Pre
) = (
    Ul
) = (
    Abbr
) = (
    B
) = (
    Bdi
) = (
    Bdo
) = (
    Br
) = (
    Cite
) = (
    Code
) = (
    Data
) = (
    Dfn
) = (
    Em
) = (
    I
) = (
    Kbd
) = (
    Mark
) = (
    Q
) = (
    Rb
) = (
    Rp
) = (
    Rt
) = (
    Rtc
) = (
    Ruby
) = (
    S
) = (
    Samp
) = (
    Small
) = (
    Span
) = (
    Strong
) = (
    Sub
) = (
    Sup
) = (
    Time
) = (
    Tt
) = (
    U
) = (
    Var
) = (
    Wbr
) = (
    Area
) = (
    Audio
) = (
    Img
) = (
    Map
) = (
    Track
) = (
    Video
) = (
    Embed
) = (
    Iframe
) = (
    Object
) = (
    Param
) = (
    Picture
) = (
    Source
) = (
    Del
) = (
    Ins
) = (
    Caption
) = (
    Col
) = (
    Colgroup
) = (
    Table
) = (
    Tbody
) = (
    Td
) = (
    Tfoot
) = (
    Th
) = (
    Thead
) = (
    Tr
) = (
    Button
) = Fieldset = Legend = Meter = Optgroup = Option = Progress = Details = Summary = None
Animate = (
    AnimateMotion
) = (
    AnimateTransform
) = (
    Circle
) = (
    ClipPath
) = (
    Defs
) = (
    Desc
) = (
    Discard
) = (
    Ellipse
) = (
    FeBlend
) = (
    FeColorMatrix
) = (
    FeComponentTransfer
) = (
    FeComposite
) = (
    FeConvolveMatrix
) = (
    FeDiffuseLighting
) = (
    FeDisplacementMap
) = (
    FeDistantLight
) = (
    FeDropShadow
) = (
    FeFlood
) = (
    FeFuncA
) = (
    FeFuncB
) = (
    FeFuncG
) = (
    FeFuncR
) = (
    FeGaussianBlur
) = (
    FeImage
) = (
    FeMerge
) = (
    FeMergeNode
) = (
    FeMorphology
) = (
    FeOffset
) = (
    FePointLight
) = (
    FeSpecularLighting
) = (
    FeSpotLight
) = (
    FeTile
) = (
    FeTurbulence
) = (
    Filter
) = (
    ForeignObject
) = (
    G
) = (
    Image
) = (
    Line
) = (
    LinearGradient
) = (
    Marker
) = (
    Mask
) = (
    Metadata
) = (
    Mpath
) = (
    Path
) = (
    Pattern
) = (
    Polygon
) = (
    Polyline
) = (
    RadialGradient
) = (
    Rect
) = Set = Stop = Svg = Switch = Symbol = Text = TextPath = Tspan = Use = View = None

# Tag classes defined dynamically at runtime
for tag in _tag_create_list:
    globals()[tag.capitalize()] = type(
        tag.capitalize(),
        (Div,),
        {"html_tag": tag, "attributes": _attr_dict.get(tag, [])},
    )

# **********************************
# SVG components
# https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute

# in, in2, mode
svg_tags = [
    "a",
    "animate",
    "animateMotion",
    "animateTransform",
    "audio",
    "canvas",
    "circle",
    "clipPath",
    "defs",
    "desc",
    "discard",
    "ellipse",
    "feBlend",
    "feColorMatrix",
    "feComponentTransfer",
    "feComposite",
    "feConvolveMatrix",
    "feDiffuseLighting",
    "feDisplacementMap",
    "feDistantLight",
    "feDropShadow",
    "feFlood",
    "feFuncA",
    "feFuncB",
    "feFuncG",
    "feFuncR",
    "feGaussianBlur",
    "feImage",
    "feMerge",
    "feMergeNode",
    "feMorphology",
    "feOffset",
    "fePointLight",
    "feSpecularLighting",
    "feSpotLight",
    "feTile",
    "feTurbulence",
    "filter",
    "foreignObject",
    "g",
    "iframe",
    "image",
    "line",
    "linearGradient",
    "marker",
    "mask",
    "metadata",
    "mpath",
    "path",
    "pattern",
    "polygon",
    "polyline",
    "radialGradient",
    "rect",
    "script",
    "set",
    "stop",
    "style",
    "svg",
    "switch",
    "symbol",
    "text",
    "textPath",
    "title",
    "tspan",
    "unknown",
    "use",
    "video",
    "view",
]

svg_tags_use = [
    "animate",
    "animateMotion",
    "animateTransform",
    "circle",
    "clipPath",
    "defs",
    "desc",
    "discard",
    "ellipse",
    "feBlend",
    "feColorMatrix",
    "feComponentTransfer",
    "feComposite",
    "feConvolveMatrix",
    "feDiffuseLighting",
    "feDisplacementMap",
    "feDistantLight",
    "feDropShadow",
    "feFlood",
    "feFuncA",
    "feFuncB",
    "feFuncG",
    "feFuncR",
    "feGaussianBlur",
    "feImage",
    "feMerge",
    "feMergeNode",
    "feMorphology",
    "feOffset",
    "fePointLight",
    "feSpecularLighting",
    "feSpotLight",
    "feTile",
    "feTurbulence",
    "filter",
    "foreignObject",
    "g",
    "image",
    "line",
    "linearGradient",
    "marker",
    "mask",
    "metadata",
    "mpath",
    "path",
    "pattern",
    "polygon",
    "polyline",
    "radialGradient",
    "rect",
    "set",
    "stop",
    "svg",
    "switch",
    "symbol",
    "text",
    "textPath",
    "tspan",
    "use",
    "view",
]

svg_presentation_attributes = [
    "alignment-baseline",
    "baseline-shift",
    "clip",
    "clip-path",
    "clip-rule",
    "color",
    "color-interpolation",
    "color-interpolation-filters",
    "color-profile",
    "color-rendering",
    "cursor",
    "direction",
    "display",
    "dominant-baseline",
    "enable-background",
    "fill",
    "fill-opacity",
    "fill-rule",
    "filter",
    "flood-color",
    "flood-opacity",
    "font-family",
    "font-size",
    "font-size-adjust",
    "font-stretch",
    "font-style",
    "font-variant",
    "font-weight",
    "glyph-orientation-horizontal",
    "glyph-orientation-vertical",
    "image-rendering",
    "kerning",
    "letter-spacing",
    "lighting-color",
    "marker-end",
    "marker-mid",
    "marker-start",
    "mask",
    "opacity",
    "overflow",
    "pointer-events",
    "shape-rendering",
    "stop-color",
    "stop-opacity",
    "stroke",
    "stroke-dasharray",
    "stroke-dashoffset",
    "stroke-linecap",
    "stroke-linejoin",
    "stroke-miterlimit",
    "stroke-opacity",
    "stroke-width",
    "text-anchor",
    "transform",
    "text-decoration",
    "text-rendering",
    "unicode-bidi",
    "vector-effect",
    "visibility",
    "word-spacing",
    "writing-mode",
    "cx",
    "cy",
    "r",
    "rx",
    "ry",
    "d",
    "fill",
    "transform",
]

svg_filter_attributes = [
    "height",
    "result",
    "width",
    "x",
    "y",
    "type",
    "tableValues",
    "slope",
    "intercept",
    "amplitude",
    "exponent",
    "offset",
    "xlink:href",
]

svg_animation_attributes = [
    "attributeType",
    "attributeName",
    "begin",
    "dur",
    "end",
    "min",
    "max",
    "restart",
    "repeatCount",
    "repeatDur",
    "fill",
    "calcMode",
    "values",
    "keyTimes",
    "keySplines",
    "from",
    "to",
    "by",
    "additive",
    "accumulate",
]

svg_attr_dict = {
    "a": ["download", "requiredExtensions", "role", "systemLanguage"],
    "animate": [
        "accumulate",
        "additive",
        "attributeName",
        "begin",
        "by",
        "calcMode",
        "dur",
        "end",
        "fill",
        "from",
        "href",
        "keySplines",
        "keyTimes",
        "max",
        "min",
        "repeatCount",
        "repeatDur",
        "requiredExtensions",
        "restart",
        "systemLanguage",
        "to",
        "values",
    ],
    "animateMotion": [
        "accumulate",
        "additive",
        "begin",
        "by",
        "calcMode",
        "dur",
        "end",
        "fill",
        "from",
        "href",
        "keyPoints",
        "keySplines",
        "keyTimes",
        "max",
        "min",
        "origin",
        "path",
        "repeatCount",
        "repeatDur",
        "requiredExtensions",
        "restart",
        "rotate",
        "systemLanguage",
        "to",
        "values",
    ],
    "animateTransform": [
        "accumulate",
        "additive",
        "attributeName",
        "begin",
        "by",
        "calcMode",
        "dur",
        "end",
        "fill",
        "from",
        "href",
        "keySplines",
        "keyTimes",
        "max",
        "min",
        "repeatCount",
        "repeatDur",
        "requiredExtensions",
        "restart",
        "systemLanguage",
        "to",
        "type",
        "values",
    ],
    "audio": ["requiredExtensions", "role", "systemLanguage"],
    "canvas": ["preserveAspectRatio", "requiredExtensions", "role", "systemLanguage"],
    "circle": ["pathLength", "requiredExtensions", "role", "systemLanguage"],
    "clipPath": ["clipPathUnits", "requiredExtensions", "systemLanguage"],
    "discard": ["begin", "href", "requiredExtensions", "role", "systemLanguage"],
    "ellipse": ["pathLength", "requiredExtensions", "role", "systemLanguage"],
    "feBlend": ["height", "in", "in2", "mode", "result", "width", "x", "y"],
    "feColorMatrix": ["height", "in", "result", "type", "values", "width", "x", "y"],
    "feComponentTransfer": ["height", "in", "result", "width", "x", "y"],
    "feComposite": [
        "height",
        "in",
        "in2",
        "k1",
        "k2",
        "k3",
        "k4",
        "operator",
        "result",
        "width",
        "x",
        "y",
    ],
    "feConvolveMatrix": [
        "bias",
        "divisor",
        "edgeMode",
        "height",
        "in",
        "kernelMatrix",
        "kernelUnitLength",
        "order",
        "preserveAlpha",
        "result",
        "targetX",
        "targetY",
        "width",
        "x",
        "y",
    ],
    "feDiffuseLighting": [
        "diffuseConstant",
        "height",
        "in",
        "kernelUnitLength",
        "result",
        "surfaceScale",
        "width",
        "x",
        "y",
    ],
    "feDisplacementMap": [
        "height",
        "in",
        "in2",
        "result",
        "scale",
        "width",
        "x",
        "xChannelSelector",
        "y",
        "yChannelSelector",
    ],
    "feDistantLight": ["azimuth", "elevation"],
    "feDropShadow": [
        "dx",
        "dy",
        "height",
        "in",
        "result",
        "stdDeviation",
        "width",
        "x",
        "y",
    ],
    "feFlood": ["height", "result", "width", "x", "y"],
    "feFuncA": [
        "amplitude",
        "exponent",
        "intercept",
        "offset",
        "slope",
        "tableValues",
        "type",
    ],
    "feFuncB": [
        "amplitude",
        "exponent",
        "intercept",
        "offset",
        "slope",
        "tableValues",
        "type",
    ],
    "feFuncG": [
        "amplitude",
        "exponent",
        "intercept",
        "offset",
        "slope",
        "tableValues",
        "type",
    ],
    "feFuncR": [
        "amplitude",
        "exponent",
        "intercept",
        "offset",
        "slope",
        "tableValues",
        "type",
    ],
    "feGaussianBlur": [
        "edgeMode",
        "height",
        "in",
        "result",
        "stdDeviation",
        "width",
        "x",
        "y",
    ],
    "feImage": [
        "crossorigin",
        "height",
        "href",
        "preserveAspectRatio",
        "result",
        "width",
        "x",
        "y",
    ],
    "feMerge": ["height", "result", "width", "x", "y"],
    "feMergeNode": ["in"],
    "feMorphology": ["height", "in", "operator", "radius", "result", "width", "x", "y"],
    "feOffset": ["dx", "dy", "height", "in", "result", "width", "x", "y"],
    "fePointLight": ["x", "y", "z"],
    "feSpecularLighting": [
        "height",
        "in",
        "kernelUnitLength",
        "result",
        "specularConstant",
        "specularExponent",
        "surfaceScale",
        "width",
        "x",
        "y",
    ],
    "feSpotLight": [
        "limitingConeAngle",
        "pointsAtX",
        "pointsAtY",
        "pointsAtZ",
        "specularExponent",
        "x",
        "y",
        "z",
    ],
    "feTile": ["height", "in", "result", "width", "x", "y"],
    "feTurbulence": [
        "baseFrequency",
        "height",
        "numOctaves",
        "result",
        "seed",
        "stitchTiles",
        "type",
        "width",
        "x",
        "y",
    ],
    "filter": ["filterUnits", "height", "primitiveUnits", "width", "x", "y"],
    "foreignObject": ["requiredExtensions", "role", "systemLanguage"],
    "g": ["requiredExtensions", "role", "systemLanguage"],
    "iframe": ["requiredExtensions", "role", "systemLanguage"],
    "image": [
        "crossorigin",
        "href",
        "preserveAspectRatio",
        "requiredExtensions",
        "role",
        "systemLanguage",
    ],
    "line": [
        "pathLength",
        "requiredExtensions",
        "role",
        "systemLanguage",
        "x1",
        "x2",
        "y1",
        "y2",
    ],
    "linearGradient": [
        "gradientTransform",
        "gradientUnits",
        "href",
        "spreadMethod",
        "x1",
        "x2",
        "y1",
        "y2",
    ],
    "marker": [
        "markerHeight",
        "markerUnits",
        "markerWidth",
        "orient",
        "preserveAspectRatio",
        "refX",
        "refY",
        "viewBox",
    ],
    "mask": [
        "height",
        "maskContentUnits",
        "maskUnits",
        "requiredExtensions",
        "systemLanguage",
        "width",
        "x",
        "y",
    ],
    "mpath": ["href"],
    "path": ["pathLength", "requiredExtensions", "role", "systemLanguage"],
    "pattern": [
        "height",
        "href",
        "patternContentUnits",
        "patternTransform",
        "patternUnits",
        "preserveAspectRatio",
        "viewBox",
        "width",
        "x",
        "y",
    ],
    "polygon": ["pathLength", "points", "requiredExtensions", "role", "systemLanguage"],
    "polyline": [
        "pathLength",
        "points",
        "requiredExtensions",
        "role",
        "systemLanguage",
    ],
    "radialGradient": [
        "cx",
        "cy",
        "fr",
        "fx",
        "fy",
        "gradientTransform",
        "gradientUnits",
        "href",
        "r",
        "spreadMethod",
    ],
    "rect": ["pathLength", "requiredExtensions", "role", "systemLanguage"],
    "script": ["href"],
    "set": [
        "attributeName",
        "begin",
        "dur",
        "end",
        "fill",
        "href",
        "max",
        "min",
        "repeatCount",
        "repeatDur",
        "requiredExtensions",
        "restart",
        "systemLanguage",
        "to",
    ],
    "stop": ["offset"],
    "style": ["media"],
    "svg": [
        "playbackorder",
        "preserveAspectRatio",
        "requiredExtensions",
        "role",
        "systemLanguage",
        "timelinebegin",
        "transform",
        "viewBox",
        "zoomAndPan",
        "xmlns",
        "version",
    ],
    "switch": ["requiredExtensions", "role", "systemLanguage"],
    "symbol": ["preserveAspectRatio", "refX", "refY", "role", "viewBox"],
    "text": [
        "dx",
        "dy",
        "lengthAdjust",
        "requiredExtensions",
        "role",
        "rotate",
        "systemLanguage",
        "textLength",
        "x",
        "y",
    ],
    "textPath": [
        "href",
        "lengthAdjust",
        "method",
        "path",
        "requiredExtensions",
        "role",
        "side",
        "spacing",
        "startOffset",
        "systemLanguage",
        "textLength",
    ],
    "tspan": [
        "dx",
        "dy",
        "lengthAdjust",
        "requiredExtensions",
        "role",
        "rotate",
        "systemLanguage",
        "textLength",
        "x",
        "y",
    ],
    "unknown": ["requiredExtensions", "role", "systemLanguage"],
    "use": ["href", "requiredExtensions", "role", "systemLanguage"],
    "video": ["requiredExtensions", "role", "systemLanguage"],
    "view": ["preserveAspectRatio", "role", "viewBox", "zoomAndPan"],
}

for tag in svg_tags_use:
    c_tag = tag[0].capitalize() + tag[1:]
    globals()[c_tag] = type(
        c_tag,
        (Div,),
        {
            "html_tag": tag,
            "attributes": svg_attr_dict.get(tag, [])
            + svg_presentation_attributes
            + svg_filter_attributes,
        },
    )


# *************************** end SVG components


class HTMLEntity(Span):
    # Render HTML Entities

    def __init__(self, **kwargs):
        self.entity = ""
        super().__init__(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["inner_html"] = self.entity
        return d


class Hello(Div):
    def __init__(self, **kwargs):
        self.counter = 1
        super().__init__(**kwargs)
        self.classes = "m-1 p-1 text-2xl text-center text-white bg-blue-500 hover:bg-blue-800 cursor-pointer"
        self.text = "Hello! (click me)"

        async def click(self, msg):
            self.text = f"Hello! I was clicked {self.counter} times"
            self.counter += 1

        self.on("click", click)


class QHello(Hello):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.classes = "text-h3 text-primary q-ma-md"


def component_by_tag(tag, attrs=[], **kwargs):
    # tag = tag.lower()
    if tag[0:2] == "q-":
        if tag in _tag_class_dict:
            c = _tag_class_dict[tag](**kwargs)
        else:
            raise ValueError(f"Tag not defined: {tag}")
    elif tag in JustPy.component_registry:
        attributes = JustPy.component_registry[tag]["attributes"]
        attr_dict = {}
        for attr in attrs:
            if attr[0] in attributes:
                attr_dict[attr[0]] = attr[1]
        c = JustPy.component_registry[tag]["class"](**attr_dict)
    else:
        tag_class_name = tag[0].capitalize() + tag[1:]
        try:
            c = globals()[tag_class_name](**kwargs)
        except:
            raise ValueError(f"Tag not defined: {tag}")
    return c


class AutoTable(Table):
    """
    Creates an HTML table from a list of lists
    First list is used as headers
    """

    td_classes = "border px-4 py-2 text-center"
    tr_even_classes = "bg-gray-100 "
    tr_odd_classes = ""
    th_classes = "px-4 py-2"

    def __init__(self, **kwargs):
        self.values = []
        super().__init__(**kwargs)

    def react(self, data):
        self.set_class("table-auto")
        # First row of values is header
        if self.values:
            headers = self.values[0]
            thead = Thead(a=self)
            tr = Tr(a=thead)
            for item in headers:
                Th(text=item, classes=self.th_classes, a=tr)
            tbody = Tbody(a=self)
            for i, row in enumerate(self.values[1:]):
                if i % 2 == 1:
                    tr = Tr(classes=self.tr_even_classes, a=tbody)
                else:
                    tr = Tr(classes=self.tr_odd_classes, a=tbody)
                for item in row:
                    Td(text=item, classes=self.td_classes, a=tr)


get_tag = component_by_tag


class BasicHTMLParser(HTMLParser):
    # Void elements do not need closing tag
    void_elements = [
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "keygen",
        "link",
        "menuitem",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    ]

    def __init__(self, context, **kwargs):
        super().__init__()
        self.context = context
        self.level = -1
        self.parse_id = 0
        self.start_tag = True
        self.components = []
        self.name_dict = Dict()  # After parsing holds a dict with named components
        self.dict_attribute = kwargs.get(
            "dict_attribute", "name"
        )  # Use another attribute than name
        self.root = Div(name="root")
        self.containers = []
        self.containers.append(self.root)
        self.endtag_required = True
        self.create_commands = kwargs.get(
            "create_commands", True
        )  # If True, create the justpy command list
        self.command_prefix = kwargs.get(
            "command_prefix", "jp."
        )  # Prefix for commands generated, defaults to 'jp.'
        if self.create_commands:
            # List of command strings (justpy python code to generate the element)
            self.commands = [f"root = {self.command_prefix}Div()"]
        else:
            self.commands = ""

    def parse_starttag(self, i):
        # This is the original library method with two changes to stop tags and attributes being lower case
        # This is required for the SVG tags which can be camelcase
        # https://github.com/python/cpython/blob/3.7/Lib/html/parser.py
        self.__starttag_text = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self.__starttag_text = rawdata[i:endpos]

        # Now parse the data between i+1 and j into a tag and attrs
        attrs = []
        match = tagfind_tolerant.match(rawdata, i + 1)
        assert match, "unexpected call to parse_starttag()"
        k = match.end()
        # self.lasttag = tag = match.group(1).lower() was the original
        self.lasttag = tag = match.group(1)
        while k < endpos:
            m = attrfind_tolerant.match(rawdata, k)
            if not m:
                break
            attrname, rest, attrvalue = m.group(1, 2, 3)
            if not rest:
                attrvalue = None
            elif (
                attrvalue[:1] == "'" == attrvalue[-1:]
                or attrvalue[:1] == '"' == attrvalue[-1:]
            ):
                attrvalue = attrvalue[1:-1]
            if attrvalue:
                attrvalue = unescape(attrvalue)
            # attrs.append((attrname.lower(), attrvalue)) was the original
            attrs.append((attrname, attrvalue))
            k = m.end()

        end = rawdata[k:endpos].strip()
        if end not in (">", "/>"):
            lineno, offset = self.getpos()
            if "\n" in self.__starttag_text:
                lineno = lineno + self.__starttag_text.count("\n")
                offset = len(self.__starttag_text) - self.__starttag_text.rfind("\n")
            else:
                offset = offset + len(self.__starttag_text)
            self.handle_data(rawdata[i:endpos])
            return endpos
        if end.endswith("/>"):
            # XHTML-style empty tag: <span attr="value" />
            self.handle_startendtag(tag, attrs)
        else:
            self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag)
        return endpos

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.endtag_required:
            self.handle_endtag(tag)
        else:
            self.endtag_required = True

    def handle_starttag(self, tag, attrs):
        self.level = self.level + 1
        self.parse_id += 1
        c = component_by_tag(tag, attrs)
        c.parse_id = self.parse_id
        command_string = f""
        if c is None:
            print(
                tag,
                "No such tag, Div being used instead *****************************************",
            )
            c = Div()
        for attr in attrs:
            attr = list(attr)
            attr[0] = attr[0].replace("-", "_")
            if attr[0][0] == "@":
                if attr[1] in self.context.f_locals:
                    c.on(attr[0][1:], self.context.f_locals[attr[1]])
                elif attr[1] in self.context.f_globals:
                    c.on(attr[0][1:], self.context.f_globals[attr[1]])
                else:
                    cls = JustpyBaseComponent
                    if not c.id:
                        c.id = cls.next_id
                        cls.next_id += 1
                    fn_string = f"def oneliner{c.id}(self, msg):\n {attr[1]}"  # remove first and last characters which are quotes
                    exec(fn_string)
                    c.on(attr[0][1:], locals()[f"oneliner{c.id}"])
                continue
            if attr[0][0] == ":":
                attr[0] = attr[0][1:]
                attr[1] = eval(attr[1])
            if attr[0] == "id":
                c.id = attr[1]
                continue
            if attr[1] is None:
                setattr(c, attr[0], True)
                attr[1] = True
            else:
                setattr(c, attr[0], attr[1])
            # Add to name to dict of named components. Each entry can be a list of components to allow multiple components with same name
            if attr[0] == self.dict_attribute:
                if attr[1] not in self.name_dict:
                    self.name_dict[attr[1]] = c
                else:
                    if not isinstance(self.name_dict[attr[1]], (list,)):
                        self.name_dict[attr[1]] = [self.name_dict[attr[1]]]
                    self.name_dict[attr[1]].append(c)
            if attr[0] == "class":
                c.classes = attr[1]
                attr[0] = "classes"
            # Handle attributes that are also python reserved words
            if attr[0] in ["in", "from"]:
                attr[0] = "_" + attr[0]

            if self.create_commands:
                if isinstance(attr[1], str):
                    command_string = f"{command_string}{attr[0]}='{attr[1]}', "
                else:
                    command_string = f"{command_string}{attr[0]}={attr[1]}, "

        if self.create_commands:
            if id(self.containers[-1]) == id(self.root):
                command_string = f"c{c.parse_id} = {self.command_prefix}{c.class_name}({command_string}a=root)"
            else:
                command_string = f"c{c.parse_id} = {self.command_prefix}{c.class_name}({command_string}a=c{self.containers[-1].parse_id})"
            self.commands.append(command_string)

        self.containers[-1].add_component(c)
        self.containers.append(c)

        if tag in BasicHTMLParser.void_elements:
            self.handle_endtag(tag)
            self.endtag_required = False
        else:
            self.endtag_required = True

    def handle_endtag(self, tag):
        c = self.containers.pop()
        del c.parse_id
        self.level = self.level - 1

    def handle_data(self, data):
        data = data.strip()
        if data:
            self.containers[-1].text = data
            data = data.replace("'", "\\'")
            if self.create_commands:
                self.commands[-1] = f"{self.commands[-1][:-1]}, text='{data}')"
        return

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])

    def handle_charref(self, name):
        if name.startswith("x"):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))

    def handle_decl(self, data):
        pass


def justPY_parser(html_string, context, **kwargs):
    """
    Returns root component of the parser with the name_dict as attribute.
    If root component has only one child, returns the child
    """
    parser = BasicHTMLParser(context, **kwargs)
    parser.feed(html_string)
    if len(parser.root.components) == 1:
        parser_result = parser.root.components[0]
    else:
        parser_result = parser.root
    parser_result.name_dict = parser.name_dict
    parser_result.commands = parser.commands
    parser_result.initialize(**kwargs)
    return parser_result


def parse_html(html_string, **kwargs):
    return justPY_parser(html_string, inspect.stack()[1][0], **kwargs)


def parse_html_file(html_file, **kwargs):
    with open(html_file, encoding="utf-8") as f:
        return justPY_parser(f.read(), inspect.stack()[1][0], **kwargs)


try:
    import aiofiles

    _has_aiofiles = True
except:
    _has_aiofiles = False

if _has_aiofiles:

    async def parse_html_file_async(html_file, **kwargs):
        async with aiofiles.open(html_file, encoding="utf-8") as f:
            s = await f.read()
        return justPY_parser(s, **kwargs)

else:

    async def parse_html_file_async(html_file, **kwargs):
        raise Exception("aiofiles not installed")


async def get(url, format="json"):
    async with httpx.AsyncClient() as client:
        result = await client.get(url)
    if format == "json":
        return result.json()
    else:
        return result.text


try:
    import markdown

    _has_markdown = True
except:
    _has_markdown = False


if _has_markdown:

    class Markdown(Div):

        all_markdown_extensions = [
            "extra",
            "abbr",
            "attr_list",
            "def_list",
            "fenced_code",
            "footnotes",
            "md_in_html",
            "tables",
            "admonition",
            "codehilite",
            "legacy_attrs",
            "legacy_em",
            "meta",
            "nl2br",
            "sane_lists",
            "smarty",
            "toc",
            "wikilinks",
        ]

        def __init__(self, **kwargs):
            self.markdown = ""
            self._cache = ""
            self.all_extensions = True
            self._html_result = ""
            self.inner_html = ""
            self.extensions = []
            super().__init__(**kwargs)

        def convert_object_to_dict(self):
            d = super().convert_object_to_dict()
            if "prose" not in d["classes"].split():
                d["classes"] += " prose"
            # Use all extensions if all_extensions is True and no extensions were specified
            if self.all_extensions and not self.extensions:
                self.extensions = self.all_markdown_extensions
            if self.markdown != self._cache:
                d["inner_html"] = self._html_result = markdown.markdown(
                    self.markdown, extensions=self.extensions
                )
                self._cache = self.markdown
            else:
                d["inner_html"] = self._html_result
            return d


class Equation(Div):

    vue_type = "katexjp"

    def __init__(self, **kwargs):
        self.equation = ""
        self.options = {"macros": {}}
        kwargs["temp"] = False  # Force an id to be assigned
        super().__init__(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d["equation"] = self.equation
        self.options["throwOnError"] = False
        d["options"] = self.options
        return d


def get_websocket(event_data):
    return WebPage.sockets[event_data["page_id"]][event_data["websocket_id"]]


def create_transition():
    return Dict(
        {
            "enter": "",
            "enter_start": "",
            "enter_end": "",
            "leave": "",
            "leave_start": "",
            "leave_end": "",
            "load": "",
            "load_start": "",
            "load_end": "",
        }
    )


class Styles:
    button_simple = (
        "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    )
    button_pill = (
        "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
    )
    button_outline = "bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded"
    button_bordered = "bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 border border-blue-700 rounded"
    button_disabled = "bg-blue-500 text-white font-bold py-2 px-4 rounded opacity-50 cursor-not-allowed"
    button_3d = "bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded"
    button_elevated = "bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow"

    input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    # https://www.lipsum.com /
    lorem_ipsum = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """
