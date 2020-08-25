# Forcing a Hard Reload

```python
import justpy as jp
from datetime import datetime

@jp.SetRoute('/hard_reload')
async def hard_reload():
    wp = jp.WebPage()
    wp.page_type = 'admin'
    d = jp.Div(text='Pages reloaded', classes='m-2 p-2 text-2xl', a=wp)
    for page in jp.WebPage.instances.values():
        if page.page_type == 'main':
            await page.reload()
    return wp

def main_page():
    wp = jp.WebPage()
    wp.page_type = 'main'
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    d = jp.Div(text=now, classes='m-2 p-2 text-2xl', a=wp)
    return wp

jp.justpy(main_page)
```