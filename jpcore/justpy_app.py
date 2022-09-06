'''
Created on 2022-09-02

@author: wf
'''
import asyncio
import socket
import re
import psutil
import typing
from sys import platform
from multiprocessing import Process 
from threading import Thread
# https://stackoverflow.com/questions/57412825/how-to-start-a-uvicorn-fastapi-in-background-when-testing-with-pytest
# https://github.com/encode/uvicorn/discussions/1103
# https://stackoverflow.com/questions/68603658/how-to-terminate-a-uvicorn-fastapi-application-cleanly-with-workers-2-when

class JustpyServer:
    '''
    a justpy Server
    
 
    '''
    def __init__(self,host:str=None,port:int=10000,sleep_time:float=0.5,mode:str=None,debug:bool=False):
        '''
        constructor
        
        Args:
            port(int): the port
            host(str): the host 
            sleep_time(float): the time to sleep after server process was started
            mode(str): None, direct or process. If None direct is used on MacOs and process on other platforms. 
                process mode will run the task as a process and kill it with psutils, direct will use threading and
                trying shutdown with uvicorns built in shutdown method (as of 2022-09 this leads to error messages since
                the starlette router is not shutdown properly)
            debug(bool): if True switch debugging on
        '''
        if host is None:
            host=socket.getfqdn()
            #host="127.0.0.1"
        self.host=host
        self.port=port
        self.sleep_time=sleep_time
        self.server=None
        self.proc=None
        self.thread=None
        if mode is None:
            if platform == "darwin":
                mode="direct"
            else:
                mode="process"
        self.mode=mode
        self.debug=debug
        self.running=False
    
    async def start(self,wpfunc,**kwargs):
        '''
        start a justpy server for the given webpage function wpfunc
        
        Args:
            wpfunc: the (async) function for the webpage
            
        
        '''
        # this import is actually calling code ...
        import justpy as jp
        if self.mode=="direct":
            jp.justpy(wpfunc,host=self.host,port=self.port,start_server=False,kwargs=kwargs)
            await asyncio.sleep(self.sleep_time)  # time for the server to start
            self.server=jp.getServer()
            self.thread=Thread(target=self.server.run)
            self.thread.start()
        elif self.mode=="process":
            needed_kwargs={
                    "host": self.host,
                    "port": self.port,
                    "start_server": True,
                }
            kwargs = {**needed_kwargs, **kwargs}
            self.proc = Process(
                target=jp.justpy,
                args=(wpfunc,),
                kwargs=kwargs,
            )
            self.proc.start()
        await asyncio.sleep(self.sleep_time)  # time for the server to start
 
    async def stop(self):
        '''
        stop the server
        '''
        #self.cancel()
        # https://stackoverflow.com/a/59089890/1497139
        #tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        #[task.cancel() for task in tasks]
        #await asyncio.gather(*tasks)
        # https://stackoverflow.com/questions/58133694/graceful-shutdown-of-uvicorn-starlette-app-with-websockets
        if self.server:
            #await asyncio.wait([jp.app.router.shutdown()],timeout=self.sleep_time)
            self.server.should_exit = True
            self.server.force_exit = True
            await asyncio.sleep(self.sleep_time)
            await self.server.shutdown()
        if self.thread:
            self.thread.join(timeout=self.sleep_time)
        if self.proc:
            pid = self.proc.pid
            parent = psutil.Process(pid)
            for child in parent.children(recursive=True):
                child.kill()
            self.proc.terminate()
            
    def nextServer(self):
        '''
        get another similar server with the portnumber incremented by one
        '''
        next_server=JustpyServer(port=self.port+1,host=self.host,sleep_time=self.sleep_time,mode=self.mode,debug=self.debug)
        return next_server
        
    def getUrl(self,path):
        '''
        get the url for the given path
        
        Args:
            path(str): the path
        Returns:
            str: the url for the path
        
        '''
        url=f"http://{self.host}:{self.port}{path}"
        return url

class JustpyApp:
    '''
    a justpy application 
    '''
    def __init__(self,pymodule_file,wp:typing.Callable=None,**kwargs):
        '''
        Args:
            pymodule_file(str): the python module path where the app resides
            wp(Callable): the webpage function to call
            **kwargs: further keyword arguments to pass to the webpage function
        '''
        self.pymodule_file=pymodule_file
        with open(self.pymodule_file, 'r') as sourcefile:
            self.source = sourcefile.read()
            self.checkDemo()
        self.wp=wp
        self.kwargs=kwargs
    
    def checkDemo(self):
        '''
        check whether this is a demo
        '''
        self.isDemo=False
        if "Demo(" or "Demo (" in self.source:
            endpointMatch=re.search("""Demo[ ]?[(]["'](.*)["'],(.*?)(,.*)*[)]""",self.source)
            if endpointMatch:
                self.description=endpointMatch.group(1)
                self.endpoint=endpointMatch.group(2)
                # jenkins could have /var/lib/jenkins/jobs/justpy/workspace/examples/charts_tutorial/pandas/women_majors2.py is not a demo
                modulematch=re.search('justpy/(workspace/)?(examples/.*)[.]py', self.pymodule_file)
                if modulematch:
                    self.pymodule=modulematch.group(2)
                    self.pymodule=self.pymodule.replace("/",".")
                    self.isDemo=not "lambda" in self.endpoint
                return 
        
    async def start(self,server:JustpyServer):
        '''
        start me on the given server
        
        Args:
            server(JustpyServer): the server to start 
        '''
        if self.wp is None:
            raise Exception(f"can't start {self.pymodule_file} -wp/endoint is None")
        return await server.start(self.wp)
          
    def __str__(self):
        text=f"{self.pymodule}:{self.endpoint}:{self.description}"
        return text