from .htmlcomponents import *
from .chartcomponents import *
from .gridcomponents import *
import demjson
from addict import Dict
import pandas as pd
from io import StringIO


# https://pandas.pydata.org/pandas-docs/stable/development/extending.html

@pd.api.extensions.register_dataframe_accessor("jp")
class JustPyAccessor:
    def __init__(self, df, **kwargs):
        self._validate(df)
        self.df = df

    @staticmethod
    def _validate(obj):
        pass


    def _get_column(self, col_spec):
        if isinstance(col_spec, int):
            col = self.df.iloc[:, col_spec]
        elif isinstance(col_spec, str):
            col = self.df[col_spec]
        else:
            raise TypeError('Column specification for plotting must be integer or string')
        col = col.replace([np.inf, -np.inf], [sys.float_info.max, -sys.float_info.max])
        return col.where((pd.notnull(col)), None)

    def plot(self, x, y, **kwargs):
        kind = kwargs.get('kind', 'column')
        chart = HighCharts(**kwargs)
        o = chart.options
        o.chart.type = kind
        o.chart.zoomType = 'xy'
        o.chart.panning = True
        o.chart.panKey = 'shift'
        o.title.text = kwargs.get('title', '')
        o.subtitle.text = kwargs.get('subtitle', '')
        o.plotOptions.series.stacking = kwargs.get('stacking', '')  # either normal or percent
        if kind != 'scatter':
            o.xAxis.categories = list(self._get_column(x))
        o.series = []
        for col in y:
            s = Dict()
            s.data = list(self._get_column(col)) if kind != 'scatter' else list(zip(self._get_column(x),self._get_column(col)))
            s.name = self.df.columns[col] if isinstance(col, int) else col
            o.series.append(s)
        return chart

    def ag_grid(self, **kwargs):
        grid = AgGrid(**kwargs)
        grid.load_pandas_frame(self.df)
        return grid

def read_csv_from_string(csv_string, *args):
    return pd.read_csv(StringIO(csv_string), *args)