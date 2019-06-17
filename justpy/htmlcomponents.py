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

#Metaclasses: https://stackoverflow.com/questions/41215107/programmatically-defining-a-class-type-vs-types-new-class

class JustPy:
    loop = None
    pass

class Folder:

    instances = []
    next_folder_id = 0


    def __init__(self,  **kwargs):

        self.send_all = False
        for k, v in kwargs.items():
            self.__setattr__(k,v)
        self.id = Folder.next_folder_id
        Folder.next_folder_id += 1
        self.pages = []  # list of pages in folder
        Folder.instances.append(self)
        # self.components = []

    def add_page(self, page):
        self.pages.append(page)
        page.folders.append(self)

    def add(self, page):
        self.add_page(page)

class WebPage:
    # Add page events like visibility. Do with templates?
    # TODO: Add page events like visibility. Do with templates? https://developer.mozilla.org/en-US/docs/Web/Events ad reload to page with seconds parameter
    # events: online, beforeunload, resize, scroll?, visibilitychange
    instances = {}
    sockets = {}
    next_page_id = 0
    use_websockets = True


    def __init__(self, **kwargs):
        self.dirty = False  # Indicates if page has changed
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
        self.template_file = 'tailwindsbase.html'
        self.static_template_file = 'server_render.html'
        self.components = []  # list  of components on page
        # self.sessions = []  # List of sessions page is on
        self.folders = []  # List of folders page is in
        self.graphs = []
        self.grids = []
        # if hasattr(self, 'name'):
        #     self.url = self.name   # Url to serve the page, defaults to name of web page
        self.css = ''
        self.html = ''
        self.reload_interval = None
        self.data = {}
        self.ui_framework = 'tailwind' # material etc.
        self.periodic_functions = []   # List of dicts {f: function, p: period_in_seconds)
        # WebPage.instances.append(self)
        WebPage.instances[self.page_id] = self
        for k, v in kwargs.items():
            self.__setattr__(k,v)

    def __repr__(self):
        return f'{self.__class__.__name__}(page_id: {self.page_id}, number of components: {len(self.components)}, reload interval: {self.reload_interval})'

    def add_component(self, component):
        self.components.append(component)
        return self     # Making adding to page implicit


    def delete(self):
        if self.delete_flag:
            for c in self.components:
                c.delete()
        self.components = []

    def add(self, *args):
        for component in args:
            self.add_component(component)

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


    def add_grid(self, grid):
        self.components.append(grid)
        if not (self in grid.pages):
            grid.pages.append(self)   # list of components the page is on
        self.grids.append(grid)


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
        for websocket in websocket_dict.values():
            # await websocket.send_json({'type': 'page_update', 'data': self.build_list()})
            try:
                # await websocket.send_json({'type': 'page_update', 'data': component_build})  # Change to create task?
                WebPage.loop.create_task(websocket.send_json({'type': 'page_update', 'data': component_build})) # Change to create task?
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
    instances = {}

    def __init__(self,  **kwargs): # c_name=None,

        cls = JustpyBaseComponent
        cls.instances[cls.next_id] = self
        self.id = cls.next_id
        cls.next_id += 1
        self.events = []
        self.allowed_events = []

    def delete(self):
        if not self.pages and self.delete_flag:
            JustpyBaseComponent.instances.pop(self.id, None)

    def on(self, event_type, func):

        if event_type in self.allowed_events:
            setattr(self, 'on_' + event_type, MethodType(func, self))
            self.events.append(event_type)
        else:
            raise Exception('No event of type {} supported'.format(event_type))


    def has_event_function(self, event_type):
        if getattr(self, 'on_' + event_type, None):
            return True
        else:
            return False



    async def update(self):
        component_dict = self.convert_object_to_dict()
        for page in self.pages:
            try:
                websocket_dict = WebPage.sockets[page.page_id]
            except:
                return self
            for websocket in websocket_dict.values():
                try:
                    await websocket.send_json({'type': 'component_update', 'data': component_dict})
                except:
                    print('Problem with websocket in component update, ignoring')
        return self



# https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API

class HTMLBaseComponent(JustpyBaseComponent):
    """
    Base Component for all HTML components
    """

    # https: // www.w3schools.com / tags / ref_standardattributes.asp
    # All components have these attributes + data-*
    html_global_attributes =['accesskey', 'class', 'contenteditable', 'dir', 'draggable', 'dropzone', 'hidden', 'id',
                             'lang', 'spellcheck', 'style', 'tabindex', 'title']

    attribute_list = ['id', 'vue_type', 'show', 'events', 'classes', 'style', 'attrs',
                      'html_tag', 'tooltip', 'class_name', 'event_propagation', 'inner_html']

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
        self.vue_type = 'html_component'   # VUE component name
        self.class_name = type(self).__name__
        self.html_tag = 'div'  # HTML to use inside component definition
        self.delete_flag = True
        self.attrs = {'id':  str(self.id)}    # Every component gets an ID in html
        self.inner_html = ''
        self.pages = []  # pages the component is on
        self.show = True
        self.classes = ''
        self.slot = None
        self.scoped_slots = {}   # for Quasar initially
        self.style = ''
        self.data = {}
        # self.name = 'c' + str(self.id)
        self.allowed_events = ['click', 'mouseover', 'mouseout', 'mouseenter', 'mouseleave', 'input', 'change',
                               'after', 'before', 'keydown', 'keyup', 'keypress']
        # self.events = False
        self.events = []
        self.event_propagation = True   # Should events be propogated?
        self.tooltip = None
        self.attributes = []
        self.prop_list = []   # For components from libraries like quasar. Contains both props and directives

        for k, v in kwargs.items():
            self.__setattr__(k,v)

        for e in self.allowed_events:   # Take care of events in keyword arguments. Either 'click' or 'onclick' or 'on_click' is fine
            if e in kwargs.keys():
                self.on(e, kwargs[e])
            elif 'on' + e in kwargs.keys():
                self.on(e, kwargs['on' + e])
            elif 'on_' + e in kwargs.keys():
                print(e,kwargs['on_' + e] )
                self.on(e, kwargs['on_' + e])

        for com in ['a', 'add_to']:
            if com in kwargs.keys():
                kwargs[com].add_component(self)


    def __repr__(self):
        if hasattr(self, 'components'):
            num_components = len(self.components)
        else:
            num_components = 0
        return f'{self.__class__.__name__}(id: {self.id}, html_tag: {self.html_tag}, vue_type: {self.vue_type}, number of components: {num_components})'

    def delete(self):
        if not self.pages and self.delete_flag:
            super().delete()
            # JustpyBaseComponent.instances.pop(self.id, None)

    def add_to_page(self, wp: WebPage):
        wp.add_component(self)

    def add_to(self, *args):
        for c in args:
            c.add_component(self)

    def on(self, event_type, func):

        if event_type in self.allowed_events:
            setattr(self, 'on_' + event_type, MethodType(func, self))
            self.events.append(event_type)
        else:
            raise Exception('No event of type {} supported'.format(event_type))


    def has_event_function(self, event_type):
        if getattr(self, 'on_' + event_type, None):
            return True
        else:
            return False

    def trigger_event(self, event_type, *args):  #trigger event from python side
        if event_type in self.allowed_events:
            try:
                getattr(self, 'on_' + event_type)(*args)
            except:
                raise Exception('No event of type {} callback provided'.format(event_type))  # Function was not defined
        else:
            raise Exception('No event of type {} supported'.format(event_type))

    def add_attribute(self, attr, value):
        self.attrs[attr] = value

    def add_event(self, event_type):
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
        # self.react(self.data)
        # HTMLBaseComponent.attribute_list = ['id', 'vue_type', 'show', 'events', 'classes', 'style', 'attrs',
        #                   'html_tag', 'tooltip', 'class_name', 'event_propagation', 'inner_html']
        for attr in HTMLBaseComponent.attribute_list:
            d[attr] = getattr(self, attr)
        d['directives'] = {}
        for i in self.prop_list+self.attributes:
            if i[0:2]=='v-':    #It is a directive
                try:
                    d['directives'][i[2:]] = getattr(self, i)
                except:
                    pass
                continue
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'div'
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

    #TODO: Handle inner_html. Basically if it exists that is the html
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
            s = f'{s}class="{self.classes}">{ws}'
        else:
            s = f'{s}>{ws}'
        # Add the text in the beginning if exists, need to test
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
        i = 0
        for obj in self.components:
            obj.react(self.data)
            d = obj.convert_object_to_dict()
            d['running_id'] = i
            i += 1
            object_list.append(d)
        return object_list

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()
        if hasattr(self, 'model'):
            self.model_update()
        d['object_props'] = self.build_list()
        if hasattr(self, 'text'):
            d['text'] = self.text
        return d

DivJP = Div

class Input(Div):
    # https://www.cssportal.com/style-input-range/   style an input range
    # Edge and Internet explorer do not support the input event for checkboxes and radio buttons. Need to use change instead
    # IMPORTANT: Scope of name of radio buttons is the whole page and not the form as is the standard unless form is sepcified

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
        self.attributes = ['accept', 'alt', 'autocomplete', 'autofocus', 'checked', 'dirname', 'disabled', 'form',
                       'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'height', 'list',
                       'max', 'maxlength', 'min', 'multiple', 'name', 'pattern', 'placeholder', 'readonly',
                       'required', 'size', 'src', 'step', 'type', 'value', 'width']

        self.html_tag = 'input'
        # self.events.extend(['input', 'change']) # Moved to convert object
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
            print(msg)
            self.checked = msg.checked
            # self.value = msg.value
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
            self.checked = update_value #self.model[0].data[self.model[1]]
        elif self.type=='radio':
            model_value = update_value #(self.model[0].data[self.model[1]])
            if self.form:
                Input.radio_button_set_model_update(self, self.form, model_value)
            else:
                Input.radio_button_set_model_update(self, self.model[0], model_value)
            pass
        elif self.type=='textarea':
                # self.text = update_value #(self.model[0].data[self.model[1]])     # Required for inital load
                self.value = update_value #(self.model[0].data[self.model[1]])
        else:
            # self.value = self.model[0].data[self.model[1]]
            self.value = update_value #(self.model[0].data[self.model[1]])

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()
        d['input_type'] = self.type     # Needed for vue component updated life hook and event handler
        if self.type in ['text', 'textarea']:
            d['value'] = str(self.value)
        else:
            d['value'] = self.value
        # print('value', self.value)
        d['attrs']['value'] = self.value
        d['checked'] = self.checked
        if self.type in ['radio', 'checkbox', 'select']:    # Ignore input event from radios, checkboxes and selects
            self.events.extend(['change'])
        else:
            self.events.extend(['input', 'change'])
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'form'
        self.attributes = ['accept-charset', 'action', 'autocomplete', 'enctype', 'method', 'name', 'novalidate', 'target']
        self.allowed_events += ['submit']
        def default_submit(self, msg):
            print('Form submitted ', msg)
        self.on('submit', default_submit)



class Label(Div):

    def __init__(self, **kwargs):
        self.for_component = None
        # self.form = None
        super().__init__(**kwargs)
        self.html_tag = 'label'
        self.attributes = ['for', 'form']  # In Justpy these accept components, not ids of component like in HTML

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

    def __init__(self, **kwargs):

        self.rows = '4'
        self.cols = '50'
        super().__init__(**kwargs)
        self.type = 'textarea'
        self.input_type = 'text'
        self.html_tag = 'textarea'
        self.attributes = self.attributes = ['autofocus', 'cols', 'dirname', 'disabled', 'form', 'maxlength', 'name',
                                             'placeholder', 'readonly', 'required', 'rows', 'wrap', 'value']




class Select(Input):
# Need to set value of select on creation, otherwise blank line will show on page update

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'select'
        self.attributes = ['autofocus', 'disabled', 'form', 'multiple', 'name', 'required', 'size']
        self.type = 'select'
        # self.events = ['change']
        # print(self.events)
        # self.events.remove('input')
        # need to look at options and set selected appropriately



class LinkJP(Div):


    def __init__(self, **kwargs):

        self.url = None  # The url to go to
        self.bookmark = None  # The component on page to jump to or scroll to
        self.title = ''
        self.download = None # If attribute is set, file is downloaded, only works html 5  https://www.w3schools.com/tags/att_a_download.asp
        self.target = 'self'  # _blank, _self, _parent, _top, framename
        # Whether to scroll to link  One of "auto", "instant", or "smooth". Defaults to "auto". https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView
        self.scroll = False
        self.scroll_option = 'smooth'
        self.attributes = ['download', 'href', 'hreflang', 'media', 'ping', 'rel', 'target', 'type']
        super().__init__(**kwargs)
        self.html_tag = 'a'
        # self.events = ['click']
        self.events.append('click')


    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()
        d['scroll'] = self.scroll
        d['scroll_option'] = self.scroll_option

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

A = LinkJP

class Icon(Div):


    def __init__(self, **kwargs):

        self.icon = 'dog'     # Default icon
        super().__init__(**kwargs)
        # self.text = ''  # Default text is name of


    def convert_object_to_dict(self):    # Every object needs to redefine this
        self.classes += ' fa fa-' + self.icon
        d = super().convert_object_to_dict()
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
        self.on('change', default_change)

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()
        return d



class TemplateJP(Div):

    """
        This component simply inserts html based on Jinja2 template.
        Corresponding Vue file is htmljp.js
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.template_string = ''   # The template string, input to Template function of Jinja2 pacakge

    def make_template(self):
        self.template = Template(self.template_string)  # Generate template

    def render(self):
    # Needs to be redefined for particular template
    # d['inner_html'] = self.template.render(month=self.month, day=self.day, weekday=self.weekday, year=self.year)
        pass


    def convert_object_to_dict(self):  # Every object needs to redefine this
        d = super().convert_object_to_dict()
        # Add read from file capability
        # with open('template.html.jinja2') as file_:
        #     template = Template(file_.read())
        # self.template = Template(self.template_string)  # Generate template
        # This needs to be called by user or redefined when class is inherited:
        # d['inner_html'] = self.template.render(month=self.month, day=self.day, weekday=self.weekday, year=self.year)
        return d

class GridJP(HTMLBaseComponent):

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
        # d = DivJP(style=cell_style)
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



class ModalJP(Div):

    # A flex container in the row direction

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.components = []
        # content-start items-start
        #self.classes ='z-50 fixed flex flex-wrap flex-row'
        self.classes ='fixed flex items-center justify-center'
        self.style = 'width: 100%; height: 100%;  background-color: rgba(0,0,0,0.4); z-index: 1; left: 0px; top: 0px'
        self.show = False
        # self.p = PJP()
        self.p.text = 'My modal'
        self.p.style = 'padding: 200px; transition: padding 2s;'
        self.p.classes = 'w-1/3 h-32 bg-white z-50 border-2 animated fadeInDown fast'
        self.add_component(self.p)


class CalendarDateJP(Div):


    def __init__(self, **kwargs):

        self.month = 'Jan'
        self.year = '2010'
        self.weekday = 'Sun'
        self.day = '1'
        super().__init__(**kwargs)
        self.template_string = """
        <div class="w-24 flex-no-shrink rounded-t overflow-hidden bg-white text-center m-2">
            <div class="bg-red-500 text-white py-1">
                {{ month }}
            </div>
            <div class="pt-1 border-l border-r">
                <span class="text-4xl font-bold">{{ day }}</span>
            </div>
            <div class="pb-2 px-2 border-l border-r border-b rounded-b flex justify-between">
                <span class="text-xs font-bold">{{ weekday }}</span>
                <span class="text-xs font-bold">{{ year }}</span>
            </div>
        </div>
        
        """

    def convert_object_to_dict(self):  # Every object needs to redefine this
        d = super().convert_object_to_dict()
        # Add read from file capability
        # with open('template.html.jinja2') as file_:
        #     template = Template(file_.read())
        self.template = Template(self.template_string)
        d['inner_html'] = self.template.render(month=self.month, day=self.day, weekday=self.weekday, year=self.year)
        return d


class Card1JP(TemplateJP):

    def __init__(self, **kwargs):
        self.blogger_name = 'John Smith'
        self.header = 'Can coffee make you a better developer?'
        self.entry_date = 'Aug 18'
        self.body_text = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.'
        super().__init__(**kwargs)
        self.template_string = """ 
<div class="max-w-md w-full lg:flex">
  <div class="h-48 lg:h-auto lg:w-48 flex-none bg-cover rounded-t lg:rounded-t-none lg:rounded-l text-center overflow-hidden" style="background-image: url('https://tailwindcss.com/img/card-left.jpg')" title="Woman holding a mug">
  </div>
  <div class="border-r border-b border-l border-grey-light lg:border-l-0 lg:border-t lg:border-grey-light bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal">
    <div class="mb-8">
      <p class="text-sm text-grey-dark flex items-center">
        <svg class="fill-current text-grey w-3 h-3 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path d="M4 8V6a6 6 0 1 1 12 0v2h1a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-8c0-1.1.9-2 2-2h1zm5 6.73V17h2v-2.27a2 2 0 1 0-2 0zM7 6v2h6V6a3 3 0 0 0-6 0z" />
        </svg>
        Members only
      </p>
      <div name="coffee" class="text-black font-bold text-xl mb-2">{{ header }}</div>
      <p class="text-grey-darker text-base">{{ body_text }}</p>
    </div>
    <div class="flex items-center">
      <img class="w-10 h-10 rounded-full mr-4" src="https://pbs.twimg.com/profile_images/885868801232961537/b1F6H4KC_400x400.jpg" alt="Avatar of Jonathan Reinink">
      <div class="text-sm">
        <p class="text-black leading-none">{{ blogger_name }}</p>
        <p class="text-grey-dark">{{ entry_date }}</p>
      </div>
    </div>
  </div>
            """

    def convert_object_to_dict(self):  # Every object needs to redefine this
        d = super().convert_object_to_dict()
        # Add read from file capability
        # with open('template.html.jinja2') as file_:
        #     template = Template(file_.read())
        self.template = Template(self.template_string)
        d['inner_html'] = self.template.render(header=self.header, entry_date=self.entry_date, body_text=self.body_text, blogger_name=self.blogger_name)
        return d


class Card2JP(TemplateJP):
    # https://tailwindcss.com/docs/examples/cards Card with categories
    def __init__(self, **kwargs):
        self.header = 'The Coldest Sunset'
        self.body_text = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus quia, nulla! Maiores et perferendis eaque, exercitationem praesentium nihil.'
        # Container where categories are added
        self.categories_list = ['Test']
        super().__init__(**kwargs)
        self.template_string = """ 
<div class="max-w-sm rounded overflow-hidden shadow-lg">
  <img class="w-full" src="https://tailwindcss.com/img/card-top.jpg" alt="Sunset in the mountains">
  <div class="px-6 py-4">
    <div class="font-bold text-xl mb-2">{{ header }}</div>
    <p class="text-grey-darker text-base">
      {{ body_text }}    </p>
  </div>
  <div class="px-6 py-4">
    {% for item in categories_list %}
   <span class="inline-block bg-grey-lighter rounded-full px-3 py-1 text-sm font-semibold text-grey-darker mr-2">#{{ item }}</span>
    {% endfor %}
  </div>
</div>
            """

    def convert_object_to_dict(self):  # Every object needs to redefine this
        d = super().convert_object_to_dict()
        # Add read from file capability
        # with open('template.html.jinja2') as file_:
        #     template = Template(file_.read())
        self.template = Template(self.template_string)
        d['inner_html'] = self.template.render(header=self.header, body_text=self.body_text, categories_list=self.categories_list)
        return d


_tag_class_dict = {}

# Div = DivJP
_tag_class_dict['div'] = Div
_tag_class_dict['input'] = Input
_tag_class_dict['form'] = Form
_tag_class_dict['select'] = Select
_tag_class_dict['textarea'] = TextArea
_tag_class_dict['label'] = Label
_tag_class_dict['a'] = A


#********************************** Start created classes

class Address(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'address'
        self.attributes = []


_tag_class_dict['address'] = Address


class Article(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'article'
        self.attributes = []


_tag_class_dict['article'] = Article


class Aside(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'aside'
        self.attributes = []


_tag_class_dict['aside'] = Aside


_tag_class_dict['div'] = Div


class Footer(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'footer'
        self.attributes = []


_tag_class_dict['footer'] = Footer


class Header(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'header'
        self.attributes = []


_tag_class_dict['header'] = Header


class H1(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'h1'
        self.attributes = []


_tag_class_dict['h1'] = H1


class H2(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'h2'
        self.attributes = []


_tag_class_dict['h2'] = H2


class H3(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'h3'
        self.attributes = []


_tag_class_dict['h3'] = H3


class H4(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'h4'
        self.attributes = []


_tag_class_dict['h4'] = H4


class H5(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'h5'
        self.attributes = []


_tag_class_dict['h5'] = H5


class H6(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'h6'
        self.attributes = []


_tag_class_dict['h6'] = H6


class Hgroup(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'hgroup'
        self.attributes = []


_tag_class_dict['hgroup'] = Hgroup


class Main(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'main'
        self.attributes = []


_tag_class_dict['main'] = Main


class Nav(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'nav'
        self.attributes = []


_tag_class_dict['nav'] = Nav


class Section(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'section'
        self.attributes = []


_tag_class_dict['section'] = Section


class Blockquote(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'blockquote'
        self.attributes = ['cite']


_tag_class_dict['blockquote'] = Blockquote


class Dd(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'dd'
        self.attributes = []


_tag_class_dict['dd'] = Dd


class Dl(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'dl'
        self.attributes = []


_tag_class_dict['dl'] = Dl


class Dt(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'dt'
        self.attributes = []


_tag_class_dict['dt'] = Dt


class Figcaption(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'figcaption'
        self.attributes = []


_tag_class_dict['figcaption'] = Figcaption


class Figure(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'figure'
        self.attributes = []


_tag_class_dict['figure'] = Figure


class Hr(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'hr'
        self.attributes = []


_tag_class_dict['hr'] = Hr


class Li(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'li'
        self.attributes = ['value']


_tag_class_dict['li'] = Li


class Ol(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'ol'
        self.attributes = ['reversed', 'start', 'type']


_tag_class_dict['ol'] = Ol


class P(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'p'
        self.attributes = []


_tag_class_dict['p'] = P


class Pre(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'pre'
        self.attributes = []


_tag_class_dict['pre'] = Pre


class Ul(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'ul'
        self.attributes = []


_tag_class_dict['ul'] = Ul





class Abbr(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'abbr'
        self.attributes = []


_tag_class_dict['abbr'] = Abbr


class B(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'b'
        self.attributes = []


_tag_class_dict['b'] = B


class Bdi(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'bdi'
        self.attributes = []


_tag_class_dict['bdi'] = Bdi


class Bdo(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'bdo'
        self.attributes = ['dir']


_tag_class_dict['bdo'] = Bdo


class Br(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'br'
        self.attributes = []


_tag_class_dict['br'] = Br


class Cite(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'cite'
        self.attributes = []


_tag_class_dict['cite'] = Cite


class Code(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'code'
        self.attributes = []


_tag_class_dict['code'] = Code


class Data(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'data'
        self.attributes = ['value']


_tag_class_dict['data'] = Data


class Dfn(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'dfn'
        self.attributes = []


_tag_class_dict['dfn'] = Dfn


class Em(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'em'
        self.attributes = []


_tag_class_dict['em'] = Em


class I(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'i'
        self.attributes = []


_tag_class_dict['i'] = I


class Kbd(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'kbd'
        self.attributes = []


_tag_class_dict['kbd'] = Kbd


class Mark(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'mark'
        self.attributes = []


_tag_class_dict['mark'] = Mark


class Q(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'q'
        self.attributes = ['cite']


_tag_class_dict['q'] = Q


class Rb(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'rb'
        self.attributes = []


_tag_class_dict['rb'] = Rb


class Rp(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'rp'
        self.attributes = []


_tag_class_dict['rp'] = Rp


class Rt(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'rt'
        self.attributes = []


_tag_class_dict['rt'] = Rt


class Rtc(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'rtc'
        self.attributes = []


_tag_class_dict['rtc'] = Rtc


class Ruby(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'ruby'
        self.attributes = []


_tag_class_dict['ruby'] = Ruby


class S(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 's'
        self.attributes = []


_tag_class_dict['s'] = S


class Samp(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'samp'
        self.attributes = []


_tag_class_dict['samp'] = Samp


class Small(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'small'
        self.attributes = []


_tag_class_dict['small'] = Small


class Span(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'span'
        self.attributes = []


_tag_class_dict['span'] = Span


class Strong(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'strong'
        self.attributes = []


_tag_class_dict['strong'] = Strong


class Sub(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'sub'
        self.attributes = []


_tag_class_dict['sub'] = Sub


class Sup(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'sup'
        self.attributes = []


_tag_class_dict['sup'] = Sup


class Time(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'time'
        self.attributes = ['datetime']


_tag_class_dict['time'] = Time


class Tt(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'tt'
        self.attributes = []


_tag_class_dict['tt'] = Tt


class U(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'u'
        self.attributes = []


_tag_class_dict['u'] = U


class Var(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'var'
        self.attributes = []


_tag_class_dict['var'] = Var


class Wbr(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'wbr'
        self.attributes = []


_tag_class_dict['wbr'] = Wbr


class Button(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'button'
        self.attributes = ['autofocus', 'disabled', 'form', 'formaction', 'formenctype', 'formmethod', 'formnovalidate',
                           'formtarget', 'name', 'type', 'value']


_tag_class_dict['button'] = Button


class Datalist(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'datalist'
        self.attributes = []


_tag_class_dict['datalist'] = Datalist


class Fieldset(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'fieldset'
        self.attributes = ['disabled', 'form', 'name']


_tag_class_dict['fieldset'] = Fieldset






class Legend(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'legend'
        self.attributes = []


_tag_class_dict['legend'] = Legend


class Meter(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'meter'
        self.attributes = ['form', 'high', 'low', 'max', 'min', 'optimum', 'value']


_tag_class_dict['meter'] = Meter


class Optgroup(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'optgroup'
        self.attributes = ['disabled', 'label']


_tag_class_dict['optgroup'] = Optgroup


class Option(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'option'
        self.attributes = ['disabled', 'label', 'selected', 'value']


_tag_class_dict['option'] = Option


class Output(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'output'
        self.attributes = ['for', 'form', 'name']


_tag_class_dict['output'] = Output


class Progress(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'progress'
        self.attributes = ['max', 'value']


_tag_class_dict['progress'] = Progress




class Img(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'img'
        self.attributes = ['alt', 'crossorigin', 'height', 'ismap', 'longdesc', 'sizes', 'src', 'srcset', 'usemap',
                     'width']


_tag_class_dict['img'] = Img


class Caption(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'caption'
        self.attributes = []


_tag_class_dict['caption'] = Caption


class Col(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'col'
        self.attributes = ['span']


_tag_class_dict['col'] = Col


class Colgroup(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'colgroup'
        self.attributes = ['span']


_tag_class_dict['colgroup'] = Colgroup


class Table(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'table'
        self.attributes = []


_tag_class_dict['table'] = Table


class Tbody(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'tbody'
        self.attributes = []


_tag_class_dict['tbody'] = Tbody


class Td(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'td'
        self.attributes = ['colspan', 'headers', 'rowspan']


_tag_class_dict['td'] = Td


class Tfoot(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'tfoot'
        self.attributes = []


_tag_class_dict['tfoot'] = Tfoot


class Th(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'th'
        self.attributes = ['abbr', 'colspan', 'headers', 'rowspan', 'scope', 'sorted']


_tag_class_dict['th'] = Th


class Thead(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'thead'
        self.attributes = []


_tag_class_dict['thead'] = Thead


class Tr(DivJP):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_tag = 'tr'
        self.attributes = []


_tag_class_dict['tr'] = Tr

#**********************************
#SVG compoenents
class Svg(DivJP):

    def __init__(self, **kwargs):

        # self.xmlns = 'http://www.w3.org/2000/svg'
        # self.viewBox = ''
        super().__init__(**kwargs)
        self.html_tag = 'svg'
        self.specific_attributes = ['x', 'y','xmlns', 'viewBox', 'height', 'width', 'preserveAspectRatio' ]
        self.attributes = 'clip-path clip-rule color color-interpolation color-rendering cursor display ' \
                          'fill fill-opacity fill-rule filter mask opacity pointer-events shape-rendering ' \
                          'stroke stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit ' \
                          'stroke-opacity stroke-width tabindex transform vector-effect visibility'.split() + self.specific_attributes

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()
        return d

_tag_class_dict['svg'] = Svg


class GJP(DivJP):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'g'
        # self.attributes = ['fill', 'stroke', 'stroke-width']
        self.attributes = 'clip-path clip-rule color color-interpolation color-rendering cursor display ' \
                          'fill fill-opacity fill-rule filter mask opacity pointer-events shape-rendering ' \
                          'stroke stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit ' \
                          'stroke-opacity stroke-width tabindex transform vector-effect visibility'.split()

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()

        return d

_tag_class_dict['g'] = GJP

class PolygonJP(DivJP):

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

_tag_class_dict['polygon'] = PolygonJP

class CircleJP(DivJP):

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

_tag_class_dict['circle'] = CircleJP


class StopJP(DivJP):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.html_tag = 'stop'
        self.specific_attributes = ['offset', 'stop-color', 'stop-opacity']
        self.attributes = 'clip-path clip-rule color color-interpolation color-rendering cursor display ' \
                          'fill fill-opacity fill-rule filter mask opacity pointer-events shape-rendering ' \
                          'stroke stroke-dasharray stroke-dashoffset stroke-linecap stroke-linejoin stroke-miterlimit ' \
                          'stroke-opacity stroke-width tabindex transform vector-effect visibility'.split() + self.specific_attributes

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()

        return d

_tag_class_dict['stop'] = StopJP

class Path(DivJP):

    def __init__(self, **kwargs):

        self.d = ''
        super().__init__(**kwargs)
        self.html_tag = 'path'

    def convert_object_to_dict(self):    # Every object needs to redefine this
        d = super().convert_object_to_dict()
        d['d'] = self.d
        d['attrs']['d'] = self.d
        return d

_tag_class_dict['path'] = Path

#*************************** end SVG compoents

class Hello(Div):

    def __init__(self, **kwargs):

        self.counter = 1
        super().__init__(**kwargs)
        self.classes = 'm-1 p-1 text-2xl text-center text-white bg-blue-500 hover:bg-blue-800'
        self.text = 'Hello!'

        def click(self, msg):
            self.text = f'Hello! I was clicked {self.counter} times'
            self.counter += 1

        self.on('click', click)


def component_by_tag(tag, **kwargs):

    c = None
    if tag in _tag_class_dict:
        c = _tag_class_dict[tag](**kwargs)
    else:
        print(f'Tag not defined: {tag}')
    return c

get_tag = component_by_tag

class BasicHTMLParser(HTMLParser):
    #to do: Deal with label tag parsing (for and form attributes)
    # container_tags_simple = ['div','select','option','span','p','svg','a', 'form', 'label', 'fieldset', 'button'] + SimpleComponent.quasar_tag_dict.keys()
    # quasar_tags = SimpleComponent.quasar_tag_dict.keys()

    # Void elements do not need closing tag
    void_elements = 'area base br col embed hr img input keygen link menuitem meta param source track wbr'.split()  # + quasar_void_elements

    def __init__(self, **kwargs):

        super().__init__()
        self.level = -1
        self.start_tag = True
        self.components = []
        self.name_dict = {}   # After parsing holds a dict with named components
        self.root = DivJP(name='root', **kwargs)
        self.containers = []
        self.containers.append(self.root)
        self.endtag_required = True

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
        # self.lasttag = tag = match.group(1).lower() original
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
            # attrs.append((attrname.lower(), attrvalue)) original
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
        if c is None:
            print(tag, 'No such tag, Div being used instead *****************************************')
            c = Div()
        for attr in attrs:
            if attr[0]=='id':
                continue
            if attr[1] is None:
                setattr(c, attr[0], True)
            else:
                try:
                    setattr(c, attr[0], float(attr[1]))
                except:
                    setattr(c, attr[0], attr[1])
            # Add to name to dict of named components. Each entry is a list of components to support multiple components with same name
            if attr[0]=='name':
                if attr[1] not in self.name_dict:
                    self.name_dict[attr[1]]= [c]
                else:
                    self.name_dict[attr[1]].append(c)
            if attr[0]=='class':
                c.classes = attr[1]

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
        # d = data.strip()
        # print('d: ', d, ' ', len(d))
        # if len(d) == 0:
        #     return
        self.containers[-1].text = data
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
        return parser.root.components[0]
    else:
        parser.root.name_dict = parser.name_dict
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

async def get(url):
    """
    Wrapper for requests get to simplify running a sync function in non blocking manner
    :param url: Url to fetch
    :return:
    """
    result = await JustPy.loop.run_in_executor(None, requests.get, url)
    return result.json()

def get_websocket(msg):
    websocket_dict = WebPage.sockets[msg.page.page_id]
    return websocket_dict[msg.websocket_id]

