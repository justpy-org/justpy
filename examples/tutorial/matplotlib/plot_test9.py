# Justpy Tutorial demo plot_test9 from docs/tutorial/matplotlib.md
import justpy as jp
import seaborn as sns

# All examples from https://seaborn.pydata.org/introduction.html

def create_page():
    wp = jp.WebPage(delete_flag=False)
    chart_classes = 'm-2'

    jp.Div(text='Tips Dataset', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    sns.set()
    tips = sns.load_dataset("tips")
    sns.relplot(x="total_bill", y="tip", col="time",
                hue="smoker", style="smoker", size="size",
                data=tips)
    jp.Matplotlib(a=wp, classes=chart_classes)
    sns.lmplot(x="total_bill", y="tip", col="time", hue="smoker",
               data=tips)
    jp.Matplotlib(a=wp, classes=chart_classes)
    sns.catplot(x="day", y="total_bill", hue="smoker",
                kind="swarm", data=tips)
    jp.Matplotlib(a=wp, classes=chart_classes)
    sns.catplot(x="day", y="total_bill", hue="smoker",
                kind="violin", split=True, data=tips)
    jp.Matplotlib(a=wp, classes=chart_classes)

    jp.Div(text='Dots Dataset', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    dots = sns.load_dataset("dots")
    sns.relplot(x="time", y="firing_rate", col="align",
                hue="choice", size="coherence", style="choice",
                facet_kws=dict(sharex=False),
                kind="line", legend="full", data=dots)
    jp.Matplotlib(a=wp, classes=chart_classes)

    jp.Div(text='FMRI Dataset', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    fmri = sns.load_dataset("fmri")
    sns.relplot(x="timepoint", y="signal", col="region",
                hue="event", style="event",
                kind="line", data=fmri)
    jp.Matplotlib(a=wp, classes=chart_classes)

    jp.Div(text='Iris Dataset', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    iris = sns.load_dataset("iris")
    sns.jointplot(x="sepal_length", y="petal_length", data=iris)
    jp.Matplotlib(a=wp, classes=chart_classes)
    sns.pairplot(data=iris, hue="species")
    jp.Matplotlib(a=wp, classes=chart_classes)

    return wp


wp = create_page()

def plot_test9():
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("plot_test9",plot_test9)
