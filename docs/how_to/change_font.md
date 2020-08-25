# Using Specific Fonts

The Tailwind team likes to use the Inter font. The way to do so is the following:

```python
import justpy as jp

def font_change():
    wp = jp.WebPage(template_file='tailwindui.html')
    wp.head_html = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/inter-ui@3.13.1/inter.min.css">'
    wp.css = 'body { font-family: Inter; }'
    # The text in this Div will be Inter
    jp.Div(text='The quick brown fox jumped over something', classes='m-4 text-3xl', a=wp)
    # Other fonts will be used for these Divs
    jp.Div(text='The quick brown fox jumped over something', classes='m-4 font-sans text-3xl', a=wp)
    jp.Div(text='The quick brown fox jumped over something', classes='m-4 font-serif text-3xl', a=wp)
    jp.Div(text='The quick brown fox jumped over something', classes='m-4 font-mono text-3xl', a=wp)
    return wp

jp.justpy(font_change)

```

The default font will now be Inter. If you specify a font class, the default tailwind fonts will be used.