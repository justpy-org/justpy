# Justpy Tutorial demo loading_page_no_stagger from docs/tutorial/page_events.md
import justpy as jp
import asyncio


async def page_ready_div(self, msg):
    for i in range(1, 3001):
        jp.Div(text=f"Div {i}", a=self.d, classes="border m-2 p-2 text-xs")
        if i % 100 == 0:
            await self.update()
            await asyncio.sleep(0.25)


@jp.SetRoute("/stagger")
def loading_page_stagger_test():
    wp = jp.WebPage()
    wp.on("page_ready", page_ready_div)
    wp.d = jp.Div(classes="flex flex-wrap", a=wp)
    return wp


def loading_page_no_stagger():
    wp = jp.WebPage()
    wp.d = jp.Div(classes="flex flex-wrap", a=wp)
    for i in range(1, 3001):
        jp.Div(text=f"Div {i}", a=wp.d, classes="border m-2 p-2 text-xs")
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("loading_page_no_stagger", loading_page_no_stagger)
