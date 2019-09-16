from .htmlcomponents import *
import demjson
from addict import Dict

class AgGrid(JustpyBaseComponent):

    # https://www.ag-grid.com/javascript-grid-features/

    vue_type = 'grid'
    default_grid_options = {
        'defaultColDef': {'filter': True, 'sortable': True, 'resizable': True,
                          'cellStyle': {'textAlign': 'center'}, 'headerClass': 'font-bold'},
        'columnDefs': [], 'rowData': []}


    def __init__(self, **kwargs):
        self.options = Dict(self.default_grid_options)
        self.classes = ''
        self.style = 'height: 500px; width:500px;'
        self.show = True
        self.pages = {}
        self.auto_size = True   # If True, automatically resizes columns after load to optimal fit
        self.theme = 'ag-theme-balham'  # one of ag-theme-balham, ag-theme-balham-dark, ag-theme-material
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            self.__setattr__(k,v)
        self.allowed_events = []
        if type(self.options) != Dict:
            self.options = Dict(self.options)
        for com in ['a', 'add_to']:
            if com in kwargs.keys():
                kwargs[com].add_component(self)

    def __repr__(self):
        return f'{self.__class__.__name__}(id: {self.id}, vue_type: {self.vue_type}, Grid options: {self.options})'

    def __setattr__(self, key, value):
        if key == 'options':
            if isinstance(value, str):
                self.load_json(value)
            else:
                self.__dict__[key] = value
        else:
            self.__dict__[key] = value

    def on(self, event_type, func):
        # Ag-Grid supports so many events, so no check is made for allowed events.
        setattr(self, 'on_' + event_type, MethodType(func, self))
        if event_type not in self.events:
            self.events.append(event_type)


    def add_to_page(self, wp: WebPage):
        wp.add_component(self)

    def add_to(self, *args):
        for c in args:
            c.add_component(self)

    def react(self, data):
        pass

    def load_json(self, options_string):
        self.options = Dict(demjson.decode(options_string.encode("ascii", "ignore")))
        return self.options

    def load_json_from_file(self, file_name):
        with open(file_name,'r') as f:
            self.options = Dict(demjson.decode(f.read().encode("ascii", "ignore")))
        return self.options

    def load_pandas_frame(self, df):
        self.options.columnDefs = [Dict({'field': i}) for i in df.columns]
        self.options.rowData = df.to_dict('records')

    def convert_object_to_dict(self):

        d = {}
        d['vue_type'] = self.vue_type
        d['id'] = self.id
        d['show'] = self.show
        d['classes'] = self.classes + ' ' + self.theme
        d['style'] = self.style
        d['def'] = self.options
        d['auto_size'] = self.auto_size
        d['events'] = self.events
        return d
