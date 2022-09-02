'''
Created on 2022-09-22

@author: wf
'''
import os
import re
from examples.basedemo import Demo
class JustpyApp:
    '''
    a justpy application 
    '''
    def __init__(self,pymodule_file):
        '''
        Args:
            pymodule_file(str): the python module path where the app resides
    
        '''
        self.pymodule_file=pymodule_file
        with open(self.pymodule_file, 'r') as sourcefile:
            self.source = sourcefile.read()
            self.checkDemo()
    
    def checkDemo(self):
        '''
        check whether this is a demo
        '''
        if "Demo(" or "Demo (" in self.source:
            endpointMatch=re.search("""Demo[ ]?[(]["'](.*)["'],(.*?)(,.*)*[)]""",self.source)
            if endpointMatch:
                self.description=endpointMatch.group(1)
                self.endpoint=endpointMatch.group(2)
                self.pymodule=re.search('justpy/(examples/.*)[.]py', self.pymodule_file).group(1)
                self.isDemo=not "lambda" in self.endpoint
                return 
        self.isDemo=False
        
    def start(self):
        '''
        start me
        '''
       
          
    def __str__(self):
        text=f"{self.pymodule}:{self.endpoint}:{self.description}"
        return text
       
        
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