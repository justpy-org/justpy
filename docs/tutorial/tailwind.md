# Tailwind

## Why Tailwind?

If you are not interested in CSS or design issues of web sites, you can safely skip this section and move ahead with the tutorial.

[Tailwind](https://tailwindcss.com/) is a "a utility-first CSS framework for rapidly building custom designs".

Tailwind is a great companion for JustPy because "instead of opinionated pre-designed components, Tailwind provides low-level utility classes that let you build completely custom designs without ever leaving your HTML". In practical terms, using Tailwind makes it easier to associate design with JustPy components and does not couple design with JavaScript. 

Of course, you need not use Tailwind, but it is worth your while evaluating it.  

## The Tailwind class dictionaries

The JustPy `Tailwind` class has two dictionaries: `tw_dict` and `tw_reverse_dict`

The first dictionary's keys are the Tailwind categories of utility classes and the value is a list of all utility classes in the category. The reverse dictionary keys are the utility classes and the value is the category they belong to. These dictionaries are used to implement the `set_class` and `set_classes` methods.

They can also be used to do the following:

```python
import justpy as jp

def text_colors():
    wp = jp.WebPage()
    d = jp.Div(classes='flex flex-wrap m-2', a=wp)
    for color in jp.Tailwind.tw_dict['text_color']:
        jp.Div(text=color, classes=f'{color} font-mono p-1 text-lg bg-blue-100 hover:bg-red-500 w-48', a=d)
    return wp

jp.justpy(text_colors)
```

This program shows the names and colors of all Tailwind text colors.


## Disabling Tailwind

To disable Tailwind add the following line to the configuration file justpy.env:
```python
TAILWIND = False
```

