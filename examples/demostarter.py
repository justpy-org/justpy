'''
Created on 2022-09-22

@author: wf
'''
import os
from examples.basedemo import Demo
from justpy.justpy_app import JustpyApp
        
class Demostarter:
    '''
    start justpy demos on different ports
    '''
    
    def __init__(self):
        '''
        constructor
        
        Args:
            baseport(int): the port number to start counting with
            limit(int): the maximum number of examples to start
        '''
        scriptdir =os.path.dirname(__file__)
        pymodule_files=self.findFiles(scriptdir, ".py")
        self.demos=[]
        for pymodule_file in pymodule_files:
            demo=JustpyApp(pymodule_file)
            if demo.isDemo:
                self.demos.append(demo)
                
    def start(self,baseport=11000,limit=None):
        '''
        start the demos from the given baseport optionally limitting the number of demos
        
        Args:
            baseport(int): the portnumber to start from
            limit(int): the maximum number of demos to start (default: None)
        '''
        Demo.testmode=True
        port=baseport
        for demo in self.demos:
            demo.port=port
            demo.start()
            port+=1
            if limit is not None and port-baseport>limit:
                break
        
    def findFiles(self,path:str,ext:str)->list:
        '''
        find Files with the given extension in the given path
        
        Args:
            path(str): the path to start with
            ext(str): the extension to search for
        
        Returns:
            list: a list of files found
        '''
        foundFiles=[]
        for root, _dirs, files in os.walk(path, topdown=False):
            for name in files:
                if name.endswith(ext):
                    filepath=os.path.join(root, name)
                    foundFiles.append(filepath)
        return foundFiles

demostarter=Demostarter()
for demo in demostarter.demos:
    print(demo)
demostarter.start(limit=2)