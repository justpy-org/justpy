from .htmlcomponents import *
import demjson
from addict import Dict

try:
    import numpy as np
    import pandas as pd
    from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype

    _has_pandas = True
except:
    _has_pandas = False


class AgGrid(JustpyBaseComponent):
    # https://www.ag-grid.com/javascript-grid-features/

    vue_type = 'grid'
    default_grid_options = {
        'animateRows': True,
        'rowDragManaged': True,
        'defaultColDef': {'filter': True, 'sortable': True, 'resizable': True, 'unSortIcon': True,
                          'cellStyle': {'textAlign': 'center'}, 'headerClass': 'font-bold'},
        'columnDefs': [], 'rowData': []
    }

    def __init__(self, **kwargs):
        self._options = Dict(self.default_grid_options)
        self.classes = ''
        self.style = 'height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;'
        self.show = True
        self.pages = {}
        self.auto_size = True  # If True, automatically resize columns after load to optimal fit
        self.theme = 'ag-theme-balham'  # one of ag-theme-balham, ag-theme-balham-dark, ag-theme-material
        kwargs['temp'] = False
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        self.allowed_events = []
        if not isinstance(self._options, Dict):
            self._options = Dict(self.options)
        for com in ['a', 'add_to']:
            if com in kwargs.keys():
                kwargs[com].add_component(self)

    def __repr__(self):
        return f'{self.__class__.__name__}(id: {self.id}, vue_type: {self.vue_type}, Grid options: {self.options})'

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        if isinstance(value, str):
            self.load_json(value)
        else:
            self.options = value

    def on(self, event_type, func):
        # https://www.ag-grid.com/javascript-grid-events/
        self.allowed_events.append(event_type)
        super().on(event_type, func)

    def add_to_page(self, wp: WebPage):
        wp.add_component(self)

    def add_to(self, *args):
        for c in args:
            c.add_component(self)

    def react(self, data):
        pass

    def load_json(self, options_string):
        self._options = Dict(demjson.decode(options_string.encode("ascii", "ignore")))
        return self._options

    def load_json_from_file(self, file_name):
        with open(file_name, 'r') as f:
            self._options = Dict(demjson.decode(f.read().encode("ascii", "ignore")))
        return self._options

    def load_pandas_frame(self, df):
        if not _has_pandas:
            raise AssertionError(f"Pandas not installed, cannot load frame")
        self._options.columnDefs = []
        for i in df.columns:
            if is_numeric_dtype(df[i]):
                col_filter = "agNumberColumnFilter"
            elif is_datetime64_any_dtype(df[i]):
                col_filter = "agDateColumnFilter"
            else:
                col_filter = True  # Use default filter
            self._options.columnDefs.append(Dict({'field': i, 'filter': col_filter}))
        # Change NaN and similar to None for JSON compatibility
        self._options.rowData = df.replace([np.inf, -np.inf], [sys.float_info.max, -sys.float_info.max]).where(
            pd.notnull(df), None).to_dict('records')

    def convert_object_to_dict(self):
        return {
            'vue_type': self.vue_type,
            'id': self.id,
            'show': self.show,
            'classes': self.classes + ' ' + self.theme,
            'style': self.style,
            'def': self.options,
            'auto_size': self.auto_size,
            'events': self.events,
        }
