# Justpy Tutorial demo clock_test from docs/tutorial/pushing_data.md
import justpy as jp
import time
import asyncio

wp = jp.WebPage(delete_flag=False)
clock_div = jp.Span(text='Loading...', classes='text-5xl m-1 p-1 bg-gray-300 font-mono', a=wp)

async def clock_counter():
    while True:
        clock_div.text = time.strftime("%a, %d %b %Y, %H:%M:%S", time.localtime())
        jp.run_task(wp.update())
        await asyncio.sleep(1)

async def clock_init():
    jp.run_task(clock_counter())

async def clock_test():
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("clock_test",clock_test, startup=clock_init)
