# Justpy Tutorial demo plot_test8 from docs/tutorial/matplotlib.md
import justpy as jp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# All examples from https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html

def create_page():
    wp = jp.WebPage(delete_flag=False)

    jp.Div(text='Series Plot', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    ts = ts.cumsum()
    ts.plot()
    jp.Matplotlib(a=wp)
    plt.close()

    jp.Div(text='Frame Plot', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
    df = df.cumsum()
    df.plot()
    jp.Matplotlib(a=wp)
    plt.close()

    jp.Div(text='Histogram', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df4 = pd.DataFrame({'a': np.random.randn(1000) + 1, 'b': np.random.randn(1000), 'c': np.random.randn(1000) - 1}, columns=['a', 'b', 'c'])
    df4.plot.hist(alpha=0.5)
    jp.Matplotlib(a=wp)
    plt.close()

    jp.Div(text='Multiple Subplots', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df.diff().hist(color='k', alpha=0.5, bins=50)
    jp.Matplotlib(a=wp)
    plt.close()

    jp.Div(text='Multiple Pie Charts', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df_pie = pd.DataFrame(3 * np.random.rand(4, 2),index=['a', 'b', 'c', 'd'], columns=['x', 'y'])
    df_pie.plot.pie(subplots=True, figsize=(8, 4))
    jp.Matplotlib(a=wp)
    plt.close()

    # The following example takes some time (about 10 seconds) to generate.
    jp.Div(text='Plotting Tools, Scatter Matrix', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df_scatter = pd.DataFrame(np.random.randn(1000, 4), columns=['a', 'b', 'c', 'd'])
    pd.plotting.scatter_matrix(df_scatter, alpha=0.2, figsize=(10, 10), diagonal='kde')
    jp.Matplotlib(a=wp)
    plt.close()

    return wp

wp = create_page()

def plot_test8():
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("plot_test8",plot_test8)
