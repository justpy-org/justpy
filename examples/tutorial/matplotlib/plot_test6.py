# Justpy Tutorial demo plot_test6 from docs/tutorial/matplotlib.md
import justpy as jp
import matplotlib.pyplot as plt


def add_point(self, msg):
    for chart in self.chart_list:
        chart.num_points += 1
        np = chart.num_points
        f = plt.figure(figsize=(2, 2))
        plt.plot([i * i for i in range(np)], marker='*', markersize=20, markeredgecolor='red')
        plt.title(f'This chart has {np} points')
        plt.xlabel('x data')
        plt.ylabel('y data')
        chart.set_figure(f)
        plt.close(f)

def subtract_point(self, msg):
    self.num_points -= 1
    np = self.num_points
    f = plt.figure(figsize=(2, 2))
    plt.plot([i*i for i in range(np)], marker='*', markersize=20, markeredgecolor='red')
    plt.title(f'This chart has {np} points')
    plt.xlabel('x data')
    plt.ylabel('y data')
    self.set_figure(f)
    plt.close(f)

def plot_test6():
    wp = jp.WebPage()
    f = plt.figure(figsize=(2, 2))
    plt.plot([0, 1, 4, 9], marker='*', markersize=20, markeredgecolor='red')
    plt.title('Matplotlib Example')
    plt.xlabel('x data')
    plt.ylabel('y data')
    d = jp.Div(classes='flex flex-wrap', a=wp)
    chart_list = []
    for i in range(5):
        chart = jp.Matplotlib(a=d, classes='m-1 p-2')
        chart.num_points = 4
        chart_list.append(chart)
        chart.on('click', subtract_point)

    plt.close(f)

    b = jp.Button(text='Add Point', a=wp,
                  classes='m-2 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded')
    b.chart_list = chart_list
    b.on('click', add_point)

    return wp


# initialize the demo
from  examples.basedemo import Demo
Demo ("plot_test6",plot_test6)
