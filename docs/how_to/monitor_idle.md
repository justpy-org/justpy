# Monitor Inactivity


```python
import justpy as jp
import time
import asyncio


def mouse_moved(self, msg):
    print('mouse moved')
    msg.page.start_time = time.perf_counter()
    return True

async def idle_test():
    wp = jp.WebPage()
    wp.start_time = time.perf_counter()
    d = jp.Div(style='height: 100vh', a=wp)
    d.add_event('mousemove')
    d.on('mousemove', mouse_moved)
    wp.idle_div = jp.Div(text='Idle time', classes='m-4 text-lg', a=d)

    # Has to be in request handler so can be specific per page
    async def monitor_timer():
        keep_monitoring = True
        idle_threshold = 5
        while keep_monitoring:
            try:
                await asyncio.sleep(5)
                idle_time = time.perf_counter() - wp.start_time
                if idle_time > idle_threshold:
                    wp.idle_div.text = f'Idle for {idle_time} seconds'
                    jp.run_task(wp.update())
            except:
                # When page is closed, it will be erased, the exception will occur and the task will terminate
                keep_monitoring = False

    jp.run_task(monitor_timer())

    return wp

jp.justpy(idle_test)
```