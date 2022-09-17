'''
Created on 2022-09-17

@author: wf
'''
import importlib
import os
import re
import typing
from jpcore.justpy_app import JustpyApp
from starlette.routing import request_response
from jpcore.example import ExampleSource

class JustpyDemoApp:
    """
    a justpy application
    """

    def __init__(self,examples_dir:str,pymodule_file:str, wpfunc: typing.Callable = None, debug:bool=False,**kwargs):
        """
        Args:
            examples_dir(str): the root directory for the examples
            pymodule_file(str): the python module path where the app resides
            wpfunc(Callable): the webpage function to call
            debug(bool): if True switch on debug mode
            **kwargs: further keyword arguments to pass to the webpage function
        """
        self.examples_dir=examples_dir
        self.pymodule_file = pymodule_file
        with open(self.pymodule_file, "r") as sourcefile:
            self.source = sourcefile.read()
            self.check_demo()
            self.example_source=ExampleSource.of_path(pymodule_file)
        source_file=pymodule_file
        self.source_file=source_file.replace(self.examples_dir+"/","")
        self.source_link=f"""<a href="https://github.com/justpy-org/justpy/blob/master/examples/{self.source_file}" target="_blank">{self.source_file}</a>"""
        self.video_url=None
        self.try_it_url=None
        self.name=os.path.basename(self.source_file).replace(".py","")
        self.wpfunc = wpfunc
        self.debug=debug
        self.status=""
        self.kwargs = kwargs

    def check_demo(self):
        """
        Check whether this is a demo
        """
        self.is_demo = False
        if "Demo(" or "Demo (" in self.source:
            func_match = re.search(
                """Demo[ ]?[(]["'](.*)["'],\s*(.*?)(,.*)*[)]""", self.source
            )
            if func_match:
                self.description = func_match.group(1)
                self.wpfunc_name = func_match.group(2)
                # jenkins could have /var/lib/jenkins/jobs/justpy/workspace/examples/charts_tutorial/pandas/women_majors2.py is not a demo
                module_match = re.search(
                    "justpy/(workspace/)?(examples/.*)[.]py", self.pymodule_file
                )
                if module_match:
                    self.pymodule = module_match.group(2)
                    self.pymodule = self.pymodule.replace("/", ".")
                    self.is_demo = not "lambda" in self.wpfunc_name                   
                return
            
    def video_link(self,target_url:str=None,alt:str=None,title:str=None,video_size=512):
        """
        get a video link for this demo 
        
        Args:
            target_url(str): the url the video link should refer to
            alt(str): the alt image name to display - default is derived from demo name
            title(str): the tooltip/title to show - default is derived from demo name
            video_size(int): the size of the video - default: 512
            
        """
        video_url=self.video_url
        if video_url is None: 
            video_url="https://user-images.githubusercontent.com/1336221/190849659-1f998e61-9cf7-4824-9767-6711d9d6ed56.jpg"
        if target_url is None:
            target_url=self.try_it_url if self.try_it_url is not None else self.video_url
        if alt is None:
            alt=f"animation for {self.name}"
        if title is None:
            title=f"animation for {self.name}"
        video_link=f"""<a href="{target_url}" target="_blank"><img src="{video_url}" alt="{alt}" style="width:{video_size}px;height:{video_size}px;"></a>"""
        return video_link

    def mount(self, app:JustpyApp, name:str=None):
        """
        mount me on the given app with the given name

        Args:
            app(JustpyApp): the app to mount me on
            name(str): the name to use for mounting - if None use the function name
        """
        demo_module = importlib.import_module(self.pymodule)
        self.wpfunc = getattr(demo_module, self.wpfunc_name)
        if self.wpfunc is None:
            raise Exception(f"can't start {self.pymodule_file} -wpfunc/endoint is None")
        # https://fastapi.tiangolo.com/advanced/sub-applications/
        endpoint=app.response(self.wpfunc)
        # wrap/cast the endpoint for starlettes routing
        # https://github.com/encode/starlette/issues/734
        mount_app=request_response(endpoint)
        if name is None:
            name=self.wpfunc.__name__
        if self.debug:
            print(f"mounting  {str(self)}")
        app.mount(f"/{name}",mount_app,name)

    def __str__(self):
        """
        return my string representation
        
        Returns:
            str: a text representation
        """
        text = f"{self.pymodule}({self.example_source}):{self.wpfunc_name}:{self.description}"
        return text
