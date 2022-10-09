# Drag and Drop

In version 0.0.9 initial drag and drop support has been added. This feature should be considered experimental and I welcome input on how to improve it.

In the example below, an image can be dragged and dropped between containers on screen. 

JustPy elements now support the 'dragstart', 'dragover', and 'drop' events.

```python
import justpy as jp


def drag_start(self, msg):
    print('in drag start')
    print(msg)
    msg.page.image.animation = False
    return True


def drop(self, msg):
    print('in drop')
    print(msg)
    wp = msg.page
    wp.image.animation = 'zoomIn'
    if self.index != wp.current_index:
        wp.div_list[self.index].add(wp.image)
        wp.div_list[wp.current_index].components = []
        wp.current_index = self.index


def drag_test():
    wp = jp.WebPage()
    wp.current_index = 0
    drag_options = {'drag_classes': 'text-white bg-red-500'}
    wp.image = jp.Img(src='https://www.python.org/static/community_logos/python-powered-h-140x182.png', height=100,
                      width=100, classes='border faster',  drag_options=drag_options, animation='zoomIn')
    wp.image.on('dragstart', drag_start)

    d = jp.Div(classes='flex flex-wrap', a=wp)
    wp.div_list = [jp.Div(style='height: 160px; width: 130px', classes='m-4 border-2 flex items-center justify-center', drop=drop, a=d, index=i) for i in range(30)]
    for div in wp.div_list:
        div.events.append('dragover')
    wp.div_list[0].add(wp.image)
    return wp

jp.justpy(drag_test)

```