# QRating

[Quasar Rating](https://quasar.dev/vue-components/rating) is a Component which allows users to rate items.

It generates an input event each time it is clicked with the value of the input being the rating.

```python
import justpy as jp

def rating_test():
    wp = jp.QuasarPage(data={'rating': 2})
    d = jp.Div(classes='q-pa-md', a=wp)
    rating_div = jp.Div(classes='q-gutter-y-md column', a=d)
    jp.QRating(size='1.5em', icon='thumb_up', a=rating_div, model=[wp, 'rating'])
    jp.QRating(size='2em', icon='favorite_border',color='red-7', a=rating_div, model=[wp, 'rating'])
    jp.QRating(size='2.5em', icon='create',color='purple-4', a=rating_div, model=[wp, 'rating'])
    jp.QRating(size='3em', icon='pets',color='brown-5', a=rating_div, model=[wp, 'rating'])
    jp.QRating(size='4.5em', icon='star_border',color='green-5', a=rating_div, model=[wp, 'rating'])
    jp.QRating(size='5em', icon='star_border',icon_selected='star',color='grey', a=rating_div, model=[wp, 'rating'],
               color_selected=['light-green-3', 'light-green-6', 'green', 'green-9', 'green-10'])
    jp.QRating(size='5em', icon='star_border',icon_selected='star',color='green-5', a=rating_div, model=[wp, 'rating'])
    jp.QRating(size='3.5em', max=4,color='red-5', a=rating_div, model=[wp, 'rating'],
               icon=['sentiment_very_dissatisfied', 'sentiment_dissatisfied', 'sentiment_satisfied', 'sentiment_very_satisfied'])
    return wp

jp.justpy(rating_test)

```

With tooltips

```python
import justpy as jp

def rating_test():
    wp = jp.QuasarPage()
    wp.tailwind = True
    num_stars = 3
    r = jp.QRating(size='2em', max=num_stars, color='primary', classes='m-2 p-2', a=wp, value=2, debounce=0)
    for i in range(1,num_stars + 1,1):
        t = jp.QTooltip(text=f'{i} rating')
        r.add_scoped_slot(f'tip-{i}', t)
    return wp


jp.justpy(rating_test)

```