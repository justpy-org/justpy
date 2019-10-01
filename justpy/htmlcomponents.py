# https://dev.to/apcelent/deploying-flask-on-aws-lambda-4k42
# https://serverless.com/framework/    https://www.zappa.io/  two good serverless options
#Classes for components and the page_object https://qz.com/1408660/the-rise-of-python-as-seen-through-a-decade-of-stack-overflow/
from types import MethodType
import json, copy, inspect, sys, re
from html.parser import HTMLParser, tagfind_tolerant, attrfind_tolerant
from html.entities import name2codepoint
from html import unescape
from jinja2 import Template
# from graphcomponents import *
# from gridcomponents import *
# import pandas as pd
import asyncio   #https://www.aeracode.org/2018/02/19/python-async-simplified/
import aiofiles
import requests
# import aiohttp
from .tailwind import Tailwind

#TODO: Handle scroll event https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight#Determine_if_an_element_has_been_totally_scrolled
#Metaclasses: https://stackoverflow.com/questions/41215107/programmatically-defining-a-class-type-vs-types-new-class

# Dict to translate from tag to class
_tag_class_dict = {}

def parse_dict(cls):
    """
    Decorator for component class definitions that updates _tag_class_dict so that the parser can recognize new component
    Required for components not defined in this module only
    Parameters
    ----------
    cls

    Returns
    -------

    """
    _tag_class_dict[cls.html_tag] = cls
    return cls

class JustPy:
    loop = None


class WebPage:

    # Add page events like visibility. Do with templates?
    # TODO: Add page events like visibility. Do with templates? https://developer.mozilla.org/en-US/docs/Web/Events ad reload to page with seconds parameter
    # events: online, beforeunload, resize, scroll?, visibilitychange
    instances = {}
    sockets = {}
    next_page_id = 0
    use_websockets = True


    def __init__(self, **kwargs):
        # self.dirty = False  # Indicates if page has changed
        # self.name = name
        self.page_id = WebPage.next_page_id
        WebPage.next_page_id += 1
        # Determines whether to use VUE or just load html of page. Static cannot handle events
        # Will add semi-static that can handle some events by activating listeners or rendering onclick and sending
        # message via websocket
        self.static = False
        self.cache = None   # Holds the last result of build_list
        self.use_cache = False  # Determines whether the framework uses the cache or not
        self.delete_flag = True
        self.template_file = 'tailwind.html'
        # self.quasar = False
        self.tailwind = True
        self.components = []  # list  of components on page
        self.folders = []  # List of folders page is in
        self.graphs = []
        self.grids = []
        self.css = ''
        self.scripts = ''
        self.html = ''
        self.body_style = ''
        self.body_classes = ''
        self.reload_interval = None
        self.data = {}
        self.ui_framework = 'tailwind' # material etc.
        self.periodic_functions = []   # List of dicts {f: function, p: period_in_seconds)
        WebPage.instances[self.page_id] = self
        for k, v in kwargs.items():
            self.__setattr__(k,v)

    def __repr__(self):
        return f'{self.__class__.__name__}(page_id: {self.page_id}, number of components: {len(self.components)}, reload interval: {self.reload_interval})'

    def __len__(self):
        return len(self.components)

    def add_component(self, component):
        self.components.append(component)
        return self     # Making adding to page implicit

    async def on_disconnect(self, websocket=None):
        pass

    def remove_page(self):
        """
        Remove page from instance dict of WebPages
        Returns
        -------

        """
        WebPage.instances.pop(self.page_id)

    def delete(self):
        if self.delete_flag:
            for c in self.components:
                c.delete()
        self.components = []

    def add(self, *args):
        for component in args:
            self.add_component(component)
        return self

    def __add__(self, other):
        # Check if list and then add each component in list
        self.add_component(other)

    def __iadd__(self, other):
        self.add_component(other)

    def remove_component(self, component):
        try:
            self.components.remove(component)
        except:
            raise Exception('Component cannot be removed because it was not in Webpage')
        return self

    def remove(self, component):
        self.remove_component(component)

    def get_components(self):
        return self.components

    def last(self):
        return self.components[-1]

    async def update(self):
        try:
            websocket_dict = WebPage.sockets[self.page_id]
        except:
            return self
        component_build = self.build_list()
        for websocket in list(websocket_dict.values()):
            try:
                WebPage.loop.create_task(websocket.send_json({'type': 'page_update', 'data': component_build}))
            except:
                print('Problem with websocket in page update, ignoring')
        return self


    async def delayed_update(self, delay):
        await asyncio.sleep(delay)
        return await self.update()

    def to_html(self, indent=0, indent_step=0, format=True):
        block_indent = ' '*indent
        if format:
            ws = '\n'
        else:
            ws = ''
        s = f'{block_indent}<div>{ws}'
        for c in self.components:
            s = f'{s}{c.to_html(indent + indent_step, indent_step, format)}'
        s = f'{s}{block_indent}</div>{ws}'
        return s

    def react(self):
        pass

    def build_list(self):
        object_list = []
        self.react()
        i = 0
        for obj in self.components:
            obj.react(self.data)
            d=obj.convert_object_to_dict()
            d['running_id'] = i
            i += 1
            object_list.append(d)
        self.cache = object_list
        return object_list


class JustpyBaseComponent(Tailwind):

    next_id = 0
    # Should instnaces be made a weakref.WeakValueDictionary? Would that help garbage collection?
    instances = {}
    # Set this to true if you want all components to be temporary by default
    temp_flag = False

    def __init__(self,  **kwargs): # c_name=None,

        temp = kwargs.get('temp', JustpyBaseComponent.temp_flag)
        # If object is not a temporary one
        if not temp:
            cls = JustpyBaseComponent
            cls.instances[cls.next_id] = self
            self.id = cls.next_id
            cls.next_id += 1
        # object is temporary and is not added to instance list
        else:
            self.id = 'temp'
        self.events = []
        self.allowed_events = []

    def delete(self):
        if self.delete_flag:
            if self.id != 'temp':
                del JustpyBaseComponent.instances[self.id]



    def on(self, event_type, func):

        if event_type in self.allowed_events:
            setattr(self, 'on_' + event_type, MethodType(func, self))
            if event_type not in self.events:
                self.events.append(event_type)
        else:
            raise Exception(f'No event of type {event_type} supported')

    def remove_event(self, event_type):
        if event_type in self.events:
            self.events.remove(event_type)

    def has_event_function(self, event_type):
        if getattr(self, 'on_' + event_type, None):
            return True
        else:
            return False

    async def update(self):
        component_dict = self.convert_object_to_dict()
        # Question: Is there a better way to iterate over a dict that may change?
        # Since the loop awaits updates, another coroutine may update the self.pages dict while the loop is running
        # Therefore, a snapshot of self.pages values is taken. This is not memory efficient. Is there another way to do this?
        pages_to_update = list(self.pages.values())
        for page in pages_to_update:
            try:
                websocket_dict = WebPage.sockets[page.page_id]
            except:
                print('No websocket dict')
                continue
                # return self
            for websocket in list(websocket_dict.values()):
                try:
                    # Use await or schedule a task? Which is the better option here?
                    # await websocket.send_json({'type': 'component_update', 'data': component_dict})
                    WebPage.loop.create_task(websocket.send_json({'type': 'component_update', 'data': component_dict}))
                except:
                    print('Problem with websocket in component update, ignoring')
        return self

    def remove_page_from_pages(self, wp: WebPage):
        self.pages.pop(wp.page_id)

    def add_page_to_pages(self, wp: WebPage):
        self.pages[wp.page_id] = wp


    @staticmethod
    def convert_dict_to_object(d):
        obj = globals()[d['class_name']]()
        for obj_prop in d['object_props']:
            obj.add(JustpyBaseComponent.convert_dict_to_object(obj_prop))
        for k, v in d.items():
            obj.__dict__[k] = v
        return obj

# https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API

class HTMLBaseComponent(JustpyBaseComponent):
    """
    Base Component for all HTML components
    """

    # https: // www.w3schools.com / tags / ref_standardattributes.asp
    # All components have these attributes + data-*
    attributes = []
    html_tag = 'div'
    vue_type = 'html_component'  # VUE component name

    html_global_attributes =['accesskey', 'class', 'contenteditable', 'dir', 'draggable', 'dropzone', 'hidden', 'id',
                             'lang', 'spellcheck', 'style', 'tabindex', 'title']

    attribute_list = ['id', 'vue_type', 'show', 'events', 'classes', 'style', 'attrs',
                      'html_tag', 'tooltip', 'class_name', 'event_propagation', 'inner_html', 'animation']

    not_initialized_attribute_list = ['accesskey', 'contenteditable', 'dir', 'draggable', 'dropzone', 'hidden',
                             'lang', 'spellcheck', 'tabindex', 'title']
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Element


    # window.addEventListener("afterprint", function(event){...});
    # window.onafterprint = function(event){...};
    windows_events = ['afterprint', 'beforeprint', 'beforeunload', 'error', 'hashchange', 'load',
                              'message', 'offline', 'online', 'pagehide', 'pageshow', 'popstate',
                              'resize', 'storage', 'unload']
    form_events = ['blur', 'change', 'contextmenu', 'focus', 'input', 'invalid', 'reset', 'search', 'select', 'submit']
    keyboard_events = ['keydown', 'keypress', 'keyup']
    mouse_events = ['click', 'dblclick', 'mousedown', 'mousemove', 'mouseout', 'mouseover', 'mouseup', 'wheel',
                    'mouseenter', 'mouseleave']

    def __init__(self,  **kwargs): # c_name=None,
        super().__init__(**kwargs)  # Important, needed to give component a unique id
        # self.vue_type = 'html_component'   # VUE component name
        self.class_name = type(self).__name__
        # self.html_tag = type(self).html_tag
        self.delete_flag = True
        self.attrs = {'id':  str(self.id)}    # Every component gets an ID in html
        self.inner_html = ''
        self.animation = False
        self.pages = {}  # pages the component is on, changed to dict
        self.show = True
        self.classes = ''
        self.slot = None
        self.scoped_slots = {}   # for Quasar initially
        self.style = ''
        self.directives = []
        self.data = {}
        # self.name = 'c' + str(self.id)
        self.allowed_events = ['click', 'mouseover', 'mouseout', 'mouseenter', 'mouseleave', 'input', 'change',
                               'after', 'before', 'keydown', 'keyup', 'keypress']
        # self.events = False
        self.events = []
        self.event_propagation = True   # Should events be propogated?
        self.tooltip = None
        # self.attributes = []
        self.attributes = type(self).attributes
        self.prop_list = []   # For components from libraries like quasar. Contains both props and directives

        for k, v in kwargs.items():
            self.__setattr__(k,v)

        for e in self.allowed_events:
            for prefix in ['', 'on', 'on_']:
                # print(kwargs.keys())
                # print(prefix, prefix + e)
                if prefix + e in kwargs.keys():
                    fn = kwargs[prefix + e]
                    if isinstance(fn, str):
                        fn_string = f'def oneliner{self.id}(self, msg):\n {fn}'
                        exec(fn_string)
                        self.on(e, locals()[f'oneliner{self.id}'])
                    else:
                        self.on(e, fn)
                    break

        for com in ['a', 'add_to']:
            if com in kwargs.keys():
                kwargs[com].add_component(self)

    def __len__(self):
        if hasattr(self, 'components'):
            return len(self.components)
        else:
            return 0

    def __repr__(self):
        return f'{self.__class__.__name__}(id: {self.id}, html_tag: {self.html_tag}, vue_type: {self.vue_type}, number of components: {len(self)})'


    def add_to_page(self, wp: WebPage):
        wp.add_component(self)

    def add_to(self, *args):
        for c in args:
            c.add_component(self)

    def on(self, event_type, func):

        if event_type in self.allowed_events:
            setattr(self, 'on_' + event_type, MethodType(func, self))
            if event_type not in self.events:
                self.events.append(event_type)
        else:
            raise Exception(f'No event of type {event_type} supported')

    def remove_event(self, event_type):
        if event_type in self.events:
            self.events.remove(event_type)


    def has_event_function(self, event_type):
        if getattr(self, 'on_' + event_type, None):
            return True
        else:
            return False

    def add_attribute(self, attr, value):
        self.attrs[attr] = value

    def add_event(self, event_type):
        # Adds an allowed event
        if event_type not in self.allowed_events:
            self.allowed_events.append(event_type)

    def add_allowed_event(self, event_type):
        # Adds an allowed event
        if event_type not in self.allowed_events:
            self.allowed_events.append(event_type)

    def add_scoped_slot(self, slot, c):
        self.scoped_slots[slot] = c

    def to_html(self, indent=0, indent_step=0, format=True):
        block_indent = ' '*indent
        if format:
            ws = '\n'
        else:
            ws = ''
        s = f'{block_indent}<{self.html_tag} '
        d = self.convert_object_to_dict()
        for attr, value in d['attrs'].items():
            s = f'{s}{attr}="{value}" '
        if self.classes:
            s = f'{s}class="{self.classes}"/>{ws}'
        else:
            s = f'{s}/>{ws}'
        return s

    # OBjects that inherit this will overwrite
    def react(self, data):
        return

    def convert_object_to_dict(self):    # Objects may need redefine this
        d = { }
        # HTMLBaseComponent.attribute_list = ['id', 'vue_type', 'show', 'events', 'classes', 'style', 'attrs',
        #                   'html_tag', 'tooltip', 'class_name', 'event_propagation', 'inner_html']
        for attr in HTMLBaseComponent.attribute_list:
            d[attr] = getattr(self, attr)
        d['directives'] = {}
        for i in self.directives:
            if i[0:2]=='v-':    #It is a directive
                try:
                    d['directives'][i[2:]] = getattr(self, i.replace('-','_'))
                except:
                    pass
        for i in self.prop_list+self.attributes:
            try:
                d['attrs'][i] = getattr(self, i)
            except:
                pass
            if '-' in i:
                s = i.replace('-','_')   # kebab case to snake case
                try:
                    d['attrs'][i] = getattr(self, s)
                except:
                    pass
        # Name is a special case. Allow it to be defined for all
        try:
            d['attrs']['name'] = self.name
        except:
            pass
        d['scoped_slots'] = {}
        for s in self.scoped_slots:
            d['scoped_slots'][s] = self.scoped_slots[s].convert_object_to_dict()
        return d



class Div(HTMLBaseComponent):

    # A general purpose container
    # This is a component that other components can be added to
    html_tag = 'div'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.components = []


    def add_component(self, child, position=None, slot=None):
        if slot:
            child.slot = slot
        if position is None:
            self.components.append(child)
        else:
            self.components.insert(position, child)
        return self


    def add(self, *args):
        for component in args:
            self.add_component(component)

    def add_first(self, child):
        self.add_component(child, 0)

    def remove_component(self, component):
        try:
            self.components.remove(component)
        except:
            raise Exception('Component cannot be removed because it is not contained')
        return self

    def remove(self, component):
        self.remove_component(component)

    def get_components(self):
        return self.components

    def first(self):
        return self.components[0]

    def last(self):
        return self.components[-1]

    def delete(self):
        if self.delete_flag:
            if self.id != 'temp':
                try:
                    del JustpyBaseComponent.instances[self.id]
                except:
                    pass
            for c in self.components:
                c.delete()


    def to_html(self, indent=0, indent_step=0, format=True):
        block_indent = ' '*indent
        if format:
            ws = '\n'
        else:
            ws = ''
        s = f'{block_indent}<{self.html_tag} '
        d = self.convert_object_to_dict()
        for attr, value in d['attrs'].items():
            s = f'{s}{attr}="{value}" '
        if self.style:
            s = f'{s}style="{self.style}"'
        if self.classes:
            s = f'{s}class="{self.classes}">{ws}'
        else:
            s = f'{s}>{ws}'
        # Add the text in the beginning if exists, need to test
        if self.inner_html:
            s = f'{s}{self.inner_html}</{self.html_tag}>{ws}'
            return s
        try:
            s = f'{s}{self.text}{ws}'
        except:
            pass
        for c in self.components:
            s = f'{s}{c.to_html(indent + indent_step, indent_step, format)}'
        s = f'{s}{block_indent}</{self.html_tag}>{ws}'
        return s


    def model_update(self):
        # [wp, 'text-data'] for example
        self.text = str(self.model[0].data[self.model[1]])

    def build_list(self):
        object_list = []
        for i, obj in enumerate(self.components):
            obj.react(self.data)
            d = obj.convert_object_to_dict()
            d['running_id'] = i
            object_list.append(d)
        return object_list

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()
        if hasattr(self, 'model'):
            self.model_update()
        d['object_props'] = self.build_list()
        if hasattr(self, 'text'):
            self.text = str(self.text)
            d['text'] = self.text
            # Handle HTML entities. Warning, they should be in their own span or div etc. Setting inner_html overrides all else in container
            if (len(self.text) > 0) and (self.text[0] == '&'):
                d['inner_html'] = self.text
        return d

class Input(Div):
    # https://www.cssportal.com/style-input-range/   style an input range
    # Edge and Internet explorer do not support the input event for checkboxes and radio buttons. Need to use change instead
    # IMPORTANT: Scope of name of radio buttons is the whole page and not the form as is the standard unless form is sepcified

    html_tag = 'input'
    attributes = ['accept', 'alt', 'autocomplete', 'autofocus', 'checked', 'dirname', 'disabled', 'form',
                  'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'height', 'list',
                  'max', 'maxlength', 'min', 'multiple', 'name', 'pattern', 'placeholder', 'readonly',
                  'required', 'size', 'src', 'step', 'type', 'value', 'width']

    def __init__(self, **kwargs):

        self.value = ''
        self.checked = False
        # Types for input element:
        # ['button', 'checkbox', 'color', 'date', 'datetime-local', 'email', 'file', 'hidden', 'image',
        # 'month', 'number', 'password', 'radio', 'range', 'reset', 'search', 'submit', 'tel', 'text', 'time', 'url', 'week']
        self.type = 'text'
        self.form = None
        # self.model = None   #[wp, 'search-text] or [d, 'search-text']
        super().__init__(**kwargs)
        # self.attributes = ['accept', 'alt', 'autocomplete', 'autofocus', 'checked', 'dirname', 'disabled', 'form',
        #                'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'height', 'list',
        #                'max', 'maxlength', 'min', 'multiple', 'name', 'pattern', 'placeholder', 'readonly',
        #                'required', 'size', 'src', 'step', 'type', 'value', 'width']

        def default_input(self, msg):
            return self.before_event_handler(msg)
        self.on('before', default_input)


    def __repr__(self):
        num_components = len(self.components)
        return f'{self.__class__.__name__}(id: {self.id}, html_tag: {self.html_tag}, input_type: {self.type}, vue_type: {self.vue_type}, value: {self.value}, checked: {self.checked}, number of components: {num_components})'

    def before_event_handler(self, msg):
        # TODO: Handle select. Works currently but may need to play with option tag children
        print('before ',self.type, msg.event_type, msg.input_type, msg)
        if msg.event_type not in ['input', 'change', 'select']:
            return
        if msg.input_type == 'checkbox':
            # The checked field is boolean
            self.checked = msg.checked
            if hasattr(self, 'model'):
                self.model[0].data[self.model[1]] = msg.checked
        elif msg.input_type == 'radio':
            # If a radio field, all other radios with same name need to have value changed
            # If form is specified, the scope is that form. If not, it is the whole page
            self.checked = True
            if self.form:
                Input.radio_button_set(self, self.form)
            else:
                Input.radio_button_set(self, msg.page)
            if hasattr(self, 'model'):
                self.model[0].data[self.model[1]] = msg.value
            self.value = msg.value
        else:
            if hasattr(self, 'model'):
                self.model[0].data[self.model[1]] = msg.value
            self.value = msg.value
        print('done before')



    @staticmethod
    def radio_button_set(radio_button, container):
        # Set all radio buttons in container with same name as radio_button to unchecked
        # print(radio_button, container)
        # print('in set radio', radio_button, radio_button.name, radio_button.id, container, container.components)
        for c in container.components:
            if hasattr(c, 'name'):
                if c.name == radio_button.name and not radio_button.id == c.id:
                    c.checked = False
            Input.radio_button_set(radio_button, c)

    @staticmethod
    def radio_button_set_model_update(radio_button, container, model_value):
        for c in container.components:
            if hasattr(c, 'name'):
                # print(c.name, c.id, c) #, c.id, c.value, c.name)
                if c.name == radio_button.name:
                    if c.value == model_value:
                        c.checked = True
                    else:
                        c.checked = False
            Input.radio_button_set_model_update(radio_button, c, model_value)


    def model_update(self):
        update_value = self.model[0].data[self.model[1]]
        if self.type=='checkbox':
            self.checked = update_value
        elif self.type=='radio':
            model_value = update_value
            if self.form:
                Input.radio_button_set_model_update(self, self.form, model_value)
            else:
                Input.radio_button_set_model_update(self, self.model[0], model_value)
        # elif self.type=='textarea':
                # self.text = update_value #(self.model[0].data[self.model[1]])     # Required for inital load
                # self.value = update_value #(self.model[0].data[self.model[1]])
        else:
            self.value = update_value

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()
        d['input_type'] = self.type     # Needed for vue component updated life hook and event handler
        if self.type in ['text', 'textarea']:
            d['value'] = str(self.value)
        else:
            d['value'] = self.value
        d['attrs']['value'] = self.value
        d['checked'] = self.checked
        if self.type in ['radio', 'checkbox', 'select']:    # Ignore input event from radios, checkboxes and selects
            if 'change' not in self.events:
                self.events.append('change')
        else:
            if ('change' not in self.events) and ('change' in self.allowed_events):
                self.events.append('change')
            if 'input' not in self.events:
                self.events.append('input')
        if self.checked:
            d['attrs']['checked'] = True
        else:
            d['attrs']['checked'] = False
        try:
            d['attrs']['form'] = self.form.id
        except:
            pass
        return d


class Form(Div):

    html_tag = 'form'
    attributes = ['accept-charset', 'action', 'autocomplete', 'enctype', 'method', 'name', 'novalidate', 'target']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allowed_events += ['submit']
        def default_submit(self, msg):
            print('Form submitted ', msg)
        self.on('submit', default_submit)


class Label(Div):

    html_tag = 'label'
    attributes = ['for', 'form']  # In Justpy these accept components, not ids of component like in HTML

    def __init__(self, **kwargs):
        self.for_component = None
        # self.form = None
        super().__init__(**kwargs)
        # self.html_tag = 'label'
        # self.attributes = ['for', 'form']  # In Justpy these accept components, not ids of component like in HTML

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        try:
            d['attrs']['for'] = self.for_component.id
        except:
            pass
        try:
            d['attrs']['form'] = self.form.id
        except:
            pass
        return d


class TextArea(Input):
    # https://www.cssportal.com/style-input-range/   style an input range

    html_tag = 'textarea'
    attributes = ['autofocus', 'cols', 'dirname', 'disabled', 'form', 'maxlength', 'name',
                  'placeholder', 'readonly', 'required', 'rows', 'wrap', 'value']

    def __init__(self, **kwargs):

        self.rows = '4'
        self.cols = '50'
        super().__init__(**kwargs)
        self.type = 'textarea'
        self.input_type = 'text'


class Select(Input):
# Need to set value of select on creation, otherwise blank line will show on page update
    html_tag = 'select'
    attributes = ['autofocus', 'disabled', 'form', 'multiple', 'name', 'required', 'size']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'select'
        # self.events = ['change']
        # need to look at options and set selected appropriately



class A(Div):

    html_tag = 'a'
    attributes = ['download', 'href', 'hreflang', 'media', 'ping', 'rel', 'target', 'type']

    def __init__(self, **kwargs):

        self.url = None  # The url to go to
        self.bookmark = None  # The component on page to jump to or scroll to
        self.title = ''
        self.download = None # If attribute is set, file is downloaded, only works html 5  https://www.w3schools.com/tags/att_a_download.asp
        self.target = 'self'  # _blank, _self, _parent, _top, framename
        # Whether to scroll to link  One of "auto", "instant", or "smooth". Defaults to "auto". https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView
        self.scroll = False
        self.scroll_option = 'smooth'  # One of "auto" or "smooth".
        self.block_option = 'start'   # One of "start", "center", "end", or "nearest". Defaults to "start".
        self.inline_option = 'nearest' # One of "start", "center", "end", or "nearest". Defaults to "nearest".
        super().__init__(**kwargs)
        self.events.append('click')


    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()

        d['scroll'] = self.scroll
        d['scroll_option'] = self.scroll_option
        d['block_option'] = self.block_option
        d['inline_option'] = self.inline_option

        if self.url:
            if self.bookmark:
                self.href = self.url + '#' + str(self.bookmark.id)   # Each component id is set to it class id which is anumber given in order of creation
            else:
                self.href = self.url
        elif self.bookmark:
            self.href = '#' + str(self.bookmark.id)
        else:
            self.href = '#'

        if self.bookmark:
            self.scroll_to = str(self.bookmark.id)        # id of element to scroll to, required by the scroll to function in EventHandler

        if d['scroll']:
            d['scroll_to'] = self.scroll_to

        d['attrs']['href'] = self.href
        d['attrs']['target'] = '_' + self.target
        if self.download is not None:
            d['attrs']['download'] = self.download

        return d

Link = A

class Icon(Div):


    def __init__(self, **kwargs):

        self.icon = 'dog'     # Default icon
        super().__init__(**kwargs)

    def convert_object_to_dict(self):
        d = super().convert_object_to_dict()
        d['classes'] = self.classes + ' fa fa-' + self.icon
        return d



class EditorJP(TextArea):
    # https://www.cssportal.com/style-input-range/   style an input range
#TODO: EditorJP, use as an example of wrapping javascript component (need to take care of javascript)
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.input_type = 'textarea'
        self.vue_type = 'editorjp'
        self.html_tag = 'textarea'
        def default_change(self, msg):
            print('in change')
            print(msg)
            # self.value = msg['value']
        # self.on('change', default_change)

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()
        return d



class Grid(HTMLBaseComponent):

    def __init__(self, **kwargs):
        # https://css-tricks.com/snippets/css/complete-guide-grid/
        self.rows = 2
        self.columns = 4
        self.column_gap = 0
        self.row_gap = 0
        # Alignemnt of items inside grid
        self.justify_items = 'stretch' # one of start, end, center, stretch    stretch is default  alignment on x axis
        self.align_items = 'stretch' # one of start, end, center, stretch    stretch is default alignment on y axis
        # Alignment if the whole grid inside its container
        self.justify_content = 'stetch' # one of start, end, center, stretch, space-around, space-between, space-evenly    stretch is default alignment on x axis
        self.align_content = 'stretch' # one of start, end, center, stretch, space-around, space-between, space-evenly    stretch is default alignment on y axis

        super().__init__(**kwargs)
        self.html_tag = 'div'
        # Components is a two dimenstional matrix
        self.components = [[Div() for x in range(self.columns)] for y in range(self.rows)]

        self.set_class('grid')
        self.style = f"""display: grid; grid-template-columns: repeat({self.columns},1fr); grid-template-rows: repeat({self.rows},1fr); 
                    grid-column-gap: {self.column_gap}px; grid-row-gap: {self.row_gap}px;
                    justify-items: {self.justify_items}; align-items: {self.align_items}; 
                    justify-content: {self.justify_content}; align-content: {self.align_content}; height: 800px;
                    """
        self.style.replace('\n','')
        self.style.replace('\t','')
        # print(self.components)


    def add_cell(self, c, row=0, col=0, num_rows=0, num_cols=0):
        c.style = f"""{c.style}; grid-column-start: {col+1}; grid-column-end: {col+1+num_cols};
                        grid-row-start: {row+1}; grid-row-end: {row+1+num_rows};
                    """
        # d = Div(style=cell_style)
        # d.add_component(c)
        self.components[row][col] = c
        return c

    def insert_pd_frame(self, pf, headers=True, index=False, cell_classes=''):
        r, c = pf.shape
        for row in range(r):
            for col in range(c):
                cell = Div(text=str(pf.iloc[row, col]), classes=cell_classes)
                self.add_cell(cell, row, col)

    def build_list(self):
        object_list = []
        i = 0
        for row in self.components:
            for obj in row:
                d = obj.convert_object_to_dict()
                d['running_id'] = i
                i += 1
                object_list.append(d)
        return object_list

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()
        d['object_props'] = self.build_list()
        return d


class Space(Div):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num = kwargs.get('num', 1)
        self.html_tag = 'span'
        self.attributes = []
        self.temp = True
        self.text = '&nbsp;' * self.num


# Non html components that are useful and should be standard

class TabGroup(Div):
    """
    Displays a tab based on its value. Has a dict of tabs whose keys is the value. A tab is any JustPy component.

    format of dict: {'value1': {'tab': comp1, 'order': number}, 'value2': {'tab': comp2, 'order': number} ...}
    self.tabs - tab dict
    self.animation_next = 'slideInRight'    set animation for tab coming in
    self.animation_prev = 'slideOutLeft'    set animation for tab going out
    self.animation_speed = 'faster'  can be on of  '' | 'slow' | 'slower' | 'fast'  | 'faster'
    self.value  value of group and tab to display
    self.previous - previous tab, no need to change except to set to '' in order to dispay tab without animation which is default at first

    """

    wrapper_classes = ' '
    wrapper_style = 'display: flex; position: absolute; width: 100%; height: 100%;  align-items: center; justify-content: center; background-color: #fff;'

    def __init__(self,  **kwargs):

        self.tabs = {}  # Dict with format 'value': {'tab': Div component, 'order': number} for each entry
        self.value = ''
        self.previous_value = ''
        # https://github.com/daneden/animate.css
        self.animation_next = 'slideInRight'
        self.animation_prev = 'slideOutLeft'
        self.animation_speed = 'faster'  # '' | 'slow' | 'slower' | 'fast'  | 'faster'

        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        if key == 'value':
            try:
                self.previous_value = self.value
            except:
                pass
        self.__dict__[key] = value


    def model_update(self):
        self.value = self.model[0].data[self.model[1]]

    def convert_object_to_dict(self):    # Every object needs to redefine this
        self.components = []
        self.wrapper_div_classes = self.animation_speed # Component in this will be centered

        if self.previous_value:
            self.wrapper_div = Div(classes=self.wrapper_div_classes, animation=self.animation_next, temp=True, style=f'{self.__class__.wrapper_style} z-index: 50;', a=self )
            self.wrapper_div.add(self.tabs[self.value]['tab'])
            self.wrapper_div = Div(classes=self.wrapper_div_classes, animation=self.animation_prev, temp=True, style=f'{self.__class__.wrapper_style} z-index: 0;', a=self)
            self.wrapper_div.add(self.tabs[self.previous_value]['tab'])
        else:
            self.wrapper_div = Div(classes=self.wrapper_div_classes, temp=True, a=self, style=self.__class__.wrapper_style)
            self.wrapper_div.add(self.tabs[self.value]['tab'])

        self.style = ' position: relative; overflow: hidden; ' + self.style  # overflow: hidden;
        d = super().convert_object_to_dict()
        return d


# HTML tags for which corresponding classes will be created
_tag_create_list = ['address', 'article', 'aside', 'footer', 'header', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'main', 'nav', 'section',
                'blockquote', 'dd', 'dl', 'dt', 'figcaption', 'figure', 'hr', 'li', 'ol', 'p', 'pre', 'ul',
                'abbr', 'b', 'bdi', 'bdo', 'br', 'cite', 'code', 'data', 'dfn', 'em', 'i', 'kbd', 'mark', 'q', 'rb',
                'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'small', 'span', 'strong', 'sub', 'sup', 'time', 'tt', 'u', 'var', 'wbr',
                'area', 'audio', 'img', 'map', 'track', 'video',
                'embed', 'iframe', 'object', 'param', 'picture', 'source',
                'del', 'ins',
                'caption', 'col', 'colgroup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr',
                'button', 'fieldset', 'legend', 'meter', 'optgroup', 'option', 'progress',  # datalist not supported
                'details', 'summary' # dialog not supported
               ]


# Only tags that have unique attributes that are supported by HTML 5 are in this dict
_attr_dict = {'a': ['download', 'href', 'hreflang', 'media', 'ping', 'rel', 'target', 'type'],
             'area': ['alt', 'coords', 'download', 'href', 'hreflang', 'media', 'rel', 'shape', 'target', 'type'],
             'audio': ['autoplay', 'controls', 'loop', 'muted', 'preload', 'src'], 'base': ['href', 'target'],
             'bdo': ['dir'], 'blockquote': ['cite'],
             'button': ['autofocus', 'disabled', 'form', 'formaction', 'formenctype', 'formmethod',
                        'formnovalidate', 'formtarget', 'name', 'type', 'value'], 'canvas': ['height', 'width'],
             'col': ['span'], 'colgroup': ['span'], 'data': ['value'], 'del': ['cite', 'datetime'],
             'details': ['open'], 'dialog': ['open'], 'embed': ['height', 'src', 'type', 'width'],
             'fieldset': ['disabled', 'form', 'name'],
             'form': ['accept-charset', 'action', 'autocomplete', 'enctype', 'method', 'name', 'novalidate',
                      'target'], 'html': ['xmlns'],
             'iframe': ['height', 'name', 'sandbox', 'src', 'srcdoc', 'width'],
             'img': ['alt', 'crossorigin', 'height', 'ismap', 'longdesc', 'sizes', 'src', 'srcset', 'usemap',
                     'width'],
             'input': ['accept', 'alt', 'autocomplete', 'autofocus', 'checked', 'dirname', 'disabled', 'form',
                       'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'height', 'list',
                       'max', 'maxlength', 'min', 'multiple', 'name', 'pattern', 'placeholder', 'readonly',
                       'required', 'size', 'src', 'step', 'type', 'value', 'width'], 'ins': ['cite', 'datetime'],
             'label': ['for', 'form'], 'li': ['value'],
             'link': ['crossorigin', 'href', 'hreflang', 'media', 'rel', 'sizes', 'type'], 'map': ['name'],
             'meta': ['charset', 'content', 'http-equiv', 'name'],
             'meter': ['form', 'high', 'low', 'max', 'min', 'optimum', 'value'],
             'object': ['data', 'form', 'height', 'name', 'type', 'usemap', 'width'],
             'ol': ['reversed', 'start', 'type'], 'optgroup': ['disabled', 'label'],
             'option': ['disabled', 'label', 'selected', 'value'], 'output': ['for', 'form', 'name'],
             'param': ['name', 'value'], 'progress': ['max', 'value'], 'q': ['cite'],
             'script': ['async', 'charset', 'defer', 'src', 'type'],
             'select': ['autofocus', 'disabled', 'form', 'multiple', 'name', 'required', 'size'],
             'source': ['src', 'srcset', 'media', 'sizes', 'type'], 'style': ['media', 'type'],
             'td': ['colspan', 'headers', 'rowspan'],
             'textarea': ['autofocus', 'cols', 'dirname', 'disabled', 'form', 'maxlength', 'name', 'placeholder',
                          'readonly', 'required', 'rows', 'wrap'],
             'th': ['abbr', 'colspan', 'headers', 'rowspan', 'scope', 'sorted'], 'time': ['datetime'],
             'track': ['default', 'kind', 'label', 'src', 'srclang'],
             'video': ['autoplay', 'controls', 'height', 'loop', 'muted', 'poster', 'preload', 'src', 'width']}


# Name definition for static syntax analysers
# Classes are defined dynamically below, this is just to assist code editors

Address=Article=Aside=Footer=Header=H1=H2=H3=H4=H5=H6=Main=Nav=Section=Blockquote=Dd=Dl=Dt=Figcaption=Figure=Hr=Li=Ol=P=Pre=Ul=Abbr=B=Bdi=Bdo=Br=Cite=Code=Data=Dfn=Em=I=Kbd=Mark=Q=Rb=Rp=Rt=Rtc=Ruby=S=Samp=Small=Span=Strong=Sub=Sup=Time=Tt=U=Var=Wbr=Area=Audio=Img=Map=Track=Video=Embed=Iframe=Object=Param=Picture=Source=Del=Ins=Caption=Col=Colgroup=Table=Tbody=Td=Tfoot=Th=Thead=Tr=Button=Fieldset=Legend=Meter=Optgroup=Option=Progress=Details=Summary=None

# Tag classes defined dynamically at runtime
for tag in _tag_create_list:
    globals()[tag.capitalize()] = type(tag.capitalize(), (Div,), {'html_tag': tag, 'attributes': _attr_dict.get(tag, [])})


#**********************************
#SVG compoenents
class Svg(Div):

    attributes = ['clip-path', 'clip-rule', 'color', 'color-interpolation', 'color-rendering', 'cursor', 'display',
                  'fill', 'fill-opacity', 'fill-rule', 'filter', 'mask', 'opacity', 'pointer-events', 'shape-rendering',
                  'stroke', 'stroke-dasharray', 'stroke-dashoffset', 'stroke-linecap', 'stroke-linejoin', 'stroke-miterlimit',
                  'stroke-opacity', 'stroke-width', 'tabindex', 'transform', 'vector-effect', 'visibility',
                  'x', 'y', 'xmlns', 'viewBox', 'height', 'width', 'preserveAspectRatio']
    html_tag = 'svg'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'svg'


class GJP(Div):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'g'
        self.attributes = 'clip-path clip-rule color color-interpolation color-rendering cursor display ' \
                          'fill fill-opacity fill-rule filter mask opacity pointer-events shape-rendering ' \
                          'stroke stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit ' \
                          'stroke-opacity stroke-width tabindex transform vector-effect visibility'.split()

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()

        return d


class PolygonJP(Div):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'polygon'
        self.specific_attributes = ['points', 'pathLength']
        self.attributes = 'clip-path clip-rule color color-interpolation color-rendering cursor display ' \
                          'fill fill-opacity fill-rule filter mask opacity pointer-events shape-rendering ' \
                          'stroke stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit ' \
                          'stroke-opacity stroke-width tabindex transform vector-effect visibility'.split() + self.specific_attributes

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()

        return d


class CircleJP(Div):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'circle'
        self.specific_attributes = ['cx', 'cy', 'r' ,'pathLength']
        self.attributes = 'clip-path clip-rule color color-interpolation color-rendering cursor display ' \
                          'fill fill-opacity fill-rule filter mask opacity pointer-events shape-rendering ' \
                          'stroke stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit ' \
                          'stroke-opacity stroke-width tabindex transform vector-effect visibility'.split() + self.specific_attributes

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()

        return d


class StopJP(Div):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'stop'
        self.specific_attributes = ['offset', 'stop-color', 'stop-opacity']
        self.attributes = 'clip-path clip-rule color color-interpolation color-rendering cursor display ' \
                          'fill fill-opacity fill-rule filter mask opacity pointer-events shape-rendering ' \
                          'stroke stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit ' \
                          'stroke-opacity stroke-width tabindex transform vector-effect visibility'.split() + self.specific_attributes


class Path(Div):

    html_tag = 'path'
    attributes = ['d', 'pathLength']

    def __init__(self, **kwargs):

        self.d = ''
        super().__init__(**kwargs)


#*************************** end SVG components

class Hello(Div):

    def __init__(self, **kwargs):

        self.counter = 1
        super().__init__(**kwargs)
        self.classes = 'm-1 p-1 text-2xl text-center text-white bg-blue-500 hover:bg-blue-800 cursor-pointer'
        self.text = 'Hello! (click me)'

        def click(self, msg):
            self.text = f'Hello! I was clicked {self.counter} times'
            self.counter += 1

        self.on('click', click)


class QHello(Hello):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.classes = 'text-h3 text-primary q-ma-md'


def component_by_tag(tag, **kwargs):
    tag = tag.lower()
    if tag[0:2] == 'q-':
        if tag in _tag_class_dict:
            c = _tag_class_dict[tag](**kwargs)
        else:
            raise ValueError(f'Tag not defined: {tag}')
    else:
        tag_class_name = tag.capitalize()
        try:
            c = globals()[tag_class_name](**kwargs)
        except:
            raise ValueError(f'Tag not defined: {tag}')
    return c

def component_by_tag_old(tag, **kwargs):
    c = None
    tag = tag.lower()
    if tag in _tag_class_dict:
        c = _tag_class_dict[tag](**kwargs)
    else:
        raise ValueError(f'Tag not defined: {tag}')
    return c


get_tag = component_by_tag

class BasicHTMLParser(HTMLParser):
    #TODO: Deal with label tag parsing (for and form attributes)

    # Void elements do not need closing tag
    void_elements = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'menuitem', 'meta',
                     'param', 'source', 'track', 'wbr']

    def __init__(self, **kwargs):

        super().__init__()
        self.level = -1
        self.start_tag = True
        self.components = []
        self.commands = ["root = jp.Div(name='root')"]    # List of command strings (justpy command to generate the element)
        self.name_dict = {}   # After parsing holds a dict with named components
        self.root = Div(name='root', **kwargs)
        self.root_name = f'c{self.root.id}'
        self.containers = []
        self.containers.append(self.root)
        self.endtag_required = True
        self.command_prefix = kwargs.get('command_prefix', 'jp.')   # Prefix for commands generated, defaults to 'jp.'

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
        assert match, 'unexpected call to parse_starttag()'
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
            elif attrvalue[:1] == '\'' == attrvalue[-1:] or \
                    attrvalue[:1] == '"' == attrvalue[-1:]:
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
                offset = len(self.__starttag_text) \
                         - self.__starttag_text.rfind("\n")
            else:
                offset = offset + len(self.__starttag_text)
            self.handle_data(rawdata[i:endpos])
            return endpos
        if end.endswith('/>'):
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
        # print(self.__starttag_text)
        c = component_by_tag(tag)
        command_string = f''
        if c is None:
            print(tag, 'No such tag, Div being used instead *****************************************')
            c = Div()
        for attr in attrs:
            attr = list(attr)
            attr[0] = attr[0].replace('-', '_')
            if attr[0][0] == ':':
                # attr = list(attr)
                attr[0] = attr[0][1:]
                attr[1] = eval(attr[1])
            if attr[0]=='id':
                continue
            if attr[1] is None:
                setattr(c, attr[0], True)
                attr[1] = True
            else:
                setattr(c, attr[0], attr[1])
            # Add to name to dict of named components. Each entry is a list of components to support multiple components with same name
            if attr[0]=='name':
                if attr[1] not in self.name_dict:
                    # self.name_dict[attr[1]]= [c]
                    self.name_dict[attr[1]]= c
                else:
                    # self.name_dict[attr[1]].append(c)
                    if not isinstance(self.name_dict[attr[1]], (list,)):
                        self.name_dict[attr[1]] = [self.name_dict[attr[1]]]
                    self.name_dict[attr[1]].append(c)
            if attr[0]=='class':
                c.classes = attr[1]
                attr[0] = 'classes'
            if isinstance(attr[1], str):
                command_string = f"{command_string}{attr[0]}='{attr[1]}', "
            else:
                command_string = f'{command_string}{attr[0]}={attr[1]}, '

        if f'c{self.containers[-1].id}' == self.root_name:
            command_string = f'c{c.id} = {self.command_prefix}{c.class_name}({command_string}a=root)'
        else:
            command_string = f'c{c.id} = {self.command_prefix}{c.class_name}({command_string}a=c{self.containers[-1].id})'


        self.commands.append(command_string)
        self.containers[-1].add_component(c)
        self.containers.append(c)



        if tag in BasicHTMLParser.void_elements:
            self.handle_endtag(tag)
            self.endtag_required = False

    def handle_endtag(self, tag):
        self.containers.pop()
        # print('Level: ',self.level, "End tag  :", tag)
        self.level = self.level - 1

    def handle_data(self, data):
        data = data.strip()
        if data:
            # print('data: ', data)
            self.containers[-1].text = data
            data = data.replace("'", "\\'")
            self.commands[-1] = f"{self.commands[-1][:-1]}, text='{data}')"

        return

    def handle_comment(self, data):
        pass
        # print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)

def justPY_parser(html_string, **kwargs):
    '''
    Returns root component of the parser with the name_dict as attribute.
    If root component has only one child, returns the child
    :param html_string:
    :param kwargs:
    :return:
    '''
    parser = BasicHTMLParser(**kwargs)
    parser.feed(html_string)
    parser.root.name_dict = parser.name_dict
    if len(parser.root.components)==1:
        # If the root div has only one component, then return it instead of the root div
        parser.root.components[0].name_dict = parser.name_dict
        parser.root.components[0].commands = parser.commands
        return parser.root.components[0]
    else:
        parser.root.name_dict = parser.name_dict
        parser.root.commands = parser.commands
        return parser.root


def parse_html(html_string, **kwargs):
    return justPY_parser(html_string, **kwargs)


def parse_html_file(html_file, **kwargs):
    with open(html_file, encoding="utf-8") as f:
        return justPY_parser(f.read(), **kwargs)

async def parse_html_file_async(html_file, **kwargs):
    async with aiofiles.open(html_file, encoding="utf-8") as f:
        s = await f.read()
    return justPY_parser(s, **kwargs)

async def get(url, format='json'):
    """Wrapper for requests get function to simplify running a sync function in non blocking manner

    Parameters
    ----------
    url

    Returns
    -------
    dict
    """
    result = await JustPy.loop.run_in_executor(None, requests.get, url)
    if format == 'json':
        return result.json()
    else:
        return result.text

def get_websocket(msg):
    """Given msg, the second parameter supplied by the framework to an event, returns the websocket object
    used to connect to the page on which event occured

    Parameters
    ----------
    msg : Dict()

    Returns
    -------
    websocket
        instance of websocket class

    """
    websocket_dict = WebPage.sockets[msg.page.page_id]
    return websocket_dict[msg.websocket_id]

def set_temp_flag(flag):
    """Sets whether components are temporary ones by default"""
    JustpyBaseComponent.temp_flag = flag



