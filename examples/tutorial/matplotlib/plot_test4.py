# Justpy Tutorial demo plot_test4 from docs/tutorial/matplotlib.md
import justpy as jp
import matplotlib.pyplot as plt


def plot_test4():
    wp = jp.WebPage()
    print(f'start {plt.get_fignums()}')
    f = plt.figure()
    plt.plot([0, 1, 4, 9], marker='*', markersize=20, markeredgecolor='red')
    plt.title('Matplotlib Example')
    plt.xlabel('x data')
    plt.ylabel('y data')
    chart = jp.Matplotlib(a=wp)
    chart.num_points = 4
    plt.close(f)

    b = jp.Button(text='Add Point', a=wp,
                  classes='m-2 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded')
    b.chart = chart

    def add_point(self, msg):
        self.chart.num_points += 1
        np = self.chart.num_points
        f = plt.figure()
        plt.plot([i*i for i in range(np)], marker='*', markersize=20, markeredgecolor='red')
        plt.title(f'This chart has {np} points')
        plt.xlabel('x data')
        plt.ylabel('y data')
        self.chart.set_figure(f)
        plt.close(f)

    b.on('click', add_point)

    def subtract_point(self, msg):
        self.num_points -= 1
        np = self.num_points
        f = plt.figure()
        plt.plot([i*i for i in range(np)], marker='*', markersize=20, markeredgecolor='red')
        plt.title(f'This chart has {np} points')
        plt.xlabel('x data')
        plt.ylabel('y data')
        self.set_figure(f)
        plt.close(f)

    chart.on('click', subtract_point)

    return wp


# initialize the demo
from  examples.basedemo import Demo
Demo ("plot_test4",plot_test4)
