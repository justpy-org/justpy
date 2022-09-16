# Justpy Tutorial demo plot_test2 from docs/tutorial/matplotlib.md
import justpy as jp
import matplotlib.pyplot as plt

def plot_test2():
    wp = jp.WebPage()

    first_figure = plt.figure()
    plt.plot([0, 1, 4, 9], marker='*', markersize=20, markeredgecolor='red')
    plt.title('First Figure Showing Second')
    plt.xlabel('x data')
    plt.ylabel('y data')

    second_figure = plt.figure()
    plt.plot([0, 1, 4, 9], marker='+', markersize=20, markeredgecolor='red')
    plt.title('Second Figure Showing First')
    plt.xlabel('x data')
    plt.ylabel('y data')

    # Keyword method of setting figure
    jp.Matplotlib(figure=second_figure, a=wp)
    # Using method after creation
    c = jp.Matplotlib(a=wp)
    c.set_figure(first_figure)

    # If memory may be an issue, don't forget to close figures not in use anymore
    plt.close(first_figure)
    plt.close(second_figure)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("plot_test2",plot_test2)
