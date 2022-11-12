# Justpy Tutorial demo loading_page_staggered_demo from docs/tutorial/page_events.md
import justpy as jp
import asyncio
import time

class StaggerDemo:
    """
    Demo for staggered or no staggered loading
    """
    
    def __init__(self,div_count:int=3000,staggered:bool=False):
        """
        constructor
        """
        self.div_count=div_count
        self.staggered=staggered
        self.wp = jp.QuasarPage(tailwind=True, title="Staggered Loading demo")
        self.top_div=jp.Div(a=self.wp)
        # QSlider seems to need some room above it
        self.slider_label=jp.Span(
            text="Number of divs to load:",a=self.top_div)
        self.slider_top_margin_div=jp.Div(a=self.top_div,classes="h-10")
        margins="margin-left: 10px;margin-right: 10px;"
        jp.QSlider(a=self.top_div,  
                   classes="w-64",
                   style=margins,
                   min=200,
                   value=self.div_count,
                   max=1000,
                   label=True,
                   label_always=True,
                   markers=True,
                   step=200,
                   snap=True,
                   color="blue",
                   change=self.on_change_div_count)
        self.timer_span=jp.Span(text=f'', a=self.top_div,style=margins)
        self.button=jp.Button(text="?", a=self.top_div, click=self.on_toggle_mode, classes=jp.Styles.button_simple)
        self.main_div = jp.Div(a=self.wp,classes="flex flex-wrap")
        self.set_mode()       
        
    def set_mode(self):
        """
        set the button text according to the staggered mode
        """
        staggered_text="" if self.staggered else "Non"
        self.mode=f"{staggered_text } staggered loading"
        button_text=f"Try {self.mode}" 
        self.button.text=button_text
        
    async def on_change_div_count(self,msg):
        """
        change the div count
        """
        self.div_count=int(msg["value"])
        pass
         
    async def on_toggle_mode(self,_msg={}):
        """
        show the different staggered behavior modes
        """
        # quickly remove main div content
        self.main_div.delete_components()
        await self.wp.update()
       
        # populate according to staggered mode
        await self.populate()
        # toggle the staggered mode
        self.staggered=not self.staggered
        # set my button text accordingly
        self.set_mode()
        await self.wp.update()
        
    async def populate(self, _msg={}):
        """
        populate the screen with self.div_count divs
        in a staggered/non staggered way depending on the self.stagger state
        """
        starttime = time.time()
        for i in range(self.div_count):
            jp.Div(text=f"Div {i+1:04d}", a=self.main_div, classes="border m-2 p-2 text-xs")
            if self.staggered:
                if i % 100 == 0:
                    await self.wp.update()
                    await asyncio.sleep(0.25)
        elapsed = time.time() - starttime
        self.timer_span.text=f"{self.mode} of {self.div_count} divs took {elapsed:5.3f} s"
    
async def loading_page_staggered_demo():
    """
    show staggered/non staggered loading
    """
    stagger_demo=StaggerDemo(400)
    await stagger_demo.on_toggle_mode()
    return stagger_demo.wp    

# initialize the demo
from examples.basedemo import Demo
Demo("loading_page_staggered_demo", loading_page_staggered_demo)
