import hjson

from .htmlcomponents import *
from addict import Dict

try:
    import numpy as np
    import pandas as pd
    from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype
    from pandas import Timestamp

    _has_pandas = True
except:
    _has_pandas = False


class AgGrid(JustpyBaseComponent):
    # https://www.ag-grid.com/javascript-grid-features/

    vue_type = "grid"
    default_grid_options = {
        "animateRows": True,
        "rowDragManaged": True,
        "defaultColDef": {
            "filter": True,
            "sortable": True,
            "resizable": True,
            "unSortIcon": True,
            "cellStyle": {"textAlign": "center"},
            "headerClass": "font-bold",
        },
        "columnDefs": [],
        "rowData": [],
    }

    def __init__(self, **kwargs):
        self.options = Dict(self.default_grid_options)
        self.classes = ""
        self.style = "height: 99vh; width: 99%; margin: 0.25rem; padding: 0.25rem;"
        self.evaluate = []  # Fields for evaluation
        self.show = True
        self.pages = {}
        self.auto_size = (
            True  # If True, automatically resize columns after load to optimal fit
        )
        self.theme = "ag-theme-balham"  # one of ag-theme-balham, ag-theme-balham-dark, ag-theme-material
        self.html_columns = []
        kwargs["temp"] = False
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        self.allowed_events = []
        if type(self.options) != Dict:
            self.options = Dict(self.options)
        for com in ["a", "add_to"]:
            if com in kwargs.keys():
                kwargs[com].add_component(self)

    def __repr__(self):
        # return f'stam'
        return f"{self.__class__.__name__}(id: {self.id}, vue_type: {self.vue_type}, Grid options: {self.options})"

    def __setattr__(self, key, value):
        if key == "options":
            if isinstance(value, str):
                self.load_json(value)
            else:
                super().__setattr__(key, value)
        else:
            super().__setattr__(key, value)

    def on(self, event_type, func, **kwargs):
        # https://www.ag-grid.com/javascript-grid-events/
        self.allowed_events.append(event_type)
        super().on(event_type, func, **kwargs)

    def add_to_page(self, wp: WebPage):
        wp.add_component(self)

    def add_to(self, *args):
        for c in args:
            c.add_component(self)

    def react(self, data):
        pass

    def load_json(self, options_string):
        self.options = Dict(hjson.loads(options_string.encode("ascii", "ignore")))
        return self.options

    def load_json_from_file(self, file_name):
        with open(file_name, "r") as f:
            self.options = Dict(hjson.loads(f.read().encode("ascii", "ignore")))
        return self.options

    def load_pandas_frame(self, df):
        assert _has_pandas, f"Pandas not installed, cannot load frame"
        self.options.columnDefs = []
        for i in df.columns:
            if is_numeric_dtype(df[i]):
                col_filter = "agNumberColumnFilter"
            elif is_datetime64_any_dtype(df[i]):
                col_filter = "agDateColumnFilter"
            else:
                col_filter = True  # Use default filter
            self.options.columnDefs.append(Dict({"field": i, "filter": col_filter}))
        # Change NaN and similar to None for JSON compatibility
        self.options.rowData = (
            df.replace([np.inf, -np.inf], [sys.float_info.max, -sys.float_info.max])
            .where(pd.notnull(df), None)
            .to_dict("records")
        )

    async def run_api(self, command, page):
        await page.run_javascript(f"""cached_grid_def['g' + {self.id}].api.{command}""")

    async def select_all_rows(self, page):
        await page.run_javascript(
            f"""cached_grid_def['g' + {self.id}].api.selectAll()"""
        )

    async def deselect_rows(self, page):
        await page.run_javascript(
            f"""cached_grid_def['g' + {self.id}].api.deselectAll()"""
        )

    async def apply_transaction(self, transaction, page):
        await page.run_javascript(
            f"""cached_grid_def['g' + {self.id}].api.applyTransaction({transaction.__repr__()})"""
        )

    def convert_object_to_dict(self):
        """
        convert object to dict
        """
        d = {}
        d["vue_type"] = self.vue_type
        d["id"] = self.id
        d["show"] = self.show
        d["classes"] = self.classes + " " + self.theme
        d["style"] = self.style
        options = self.options.deepcopy()
        for row in options.get("rowData", []):
            for k, v in row.items():
                if _has_pandas and isinstance(v, Timestamp):
                    row[k] = str(v)
        d["def"] = options
        d["auto_size"] = self.auto_size
        d["events"] = self.events
        d["html_columns"] = self.html_columns
        d["evaluate"] = self.evaluate
        return d
