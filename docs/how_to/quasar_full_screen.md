# How to Toggle Full Screen Mode in Quasar

```python
import justpy as jp

async def toggle_screen(self, msg):
    await msg.page.run_javascript('Quasar.AppFullscreen.toggle()')

def full_screen_test():
    wp = jp.QuasarPage()
    d = jp.Div(classes='q-pa-md q-gutter-sm', a=wp)
    jp.QBtn(color='primary', label='Toggle Screen', a=d, click=toggle_screen)
    return wp

jp.justpy(full_screen_test)
```