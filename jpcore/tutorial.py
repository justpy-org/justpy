'''
Created on 2022-09-16

@author: wf
'''
import os
import re
from jpcore.utilities import find_files

class TutorialManager:
    """
    justpy tutorial
    """
    
    def __init__(self,docs_dir:str=None):
        """
        constructor
        
        Args:
            docs_dir(str): the path from which to read the tutorial files
        """
        self.tutorials={}
        self.script_dir = os.path.dirname(__file__)
        if docs_dir is None:
            docs_dir = f"{os.path.dirname(self.script_dir)}/docs"
        self.docs_dir=docs_dir
        self.total_lines=0
        self.total_examples=0
        self.tutorial_files = find_files(self.docs_dir, ".md")
        for tutorial_file_path in self.tutorial_files:
            tutorial=Tutorial(docs_dir,tutorial_file_path)
            self.tutorials[tutorial.name]=tutorial
            self.total_lines+=len(tutorial.lines)
            self.total_examples+=len(tutorial.examples)
        
class Tutorial:
    """
    a single tutorial file
    """
    
    def __init__(self,docs_dir,path:str):
        """
        construct me
        """
        self.examples={}
        self.path=path
        self.name=path.replace(docs_dir+"/","")
        with open(self.path, "r") as markup_file:
            self.markup = markup_file.read()
        self.lines=self.markup.split("\n")
        header=None
        for line in self.lines:
            header_match= re.search("^#+\s*(.*)",line)
            if header_match:
                header=header_match.group(1)
                pass
            justpy_match = re.search(
                """jp.justpy[(]([a-zA-Z_0-9]*)[,)]""", line
            )
            if justpy_match:
                example_name = justpy_match.group(1)
                example=Example(self,example_name,header,[])
                self.examples[example.name]=example
                header=None

class Example:
    """
    an example
    """
    
    def __init__(self,tutorial:Tutorial,name:str,header:str,lines:list):
        """
        constructor
        
        Args:
            tutorial(Tutorial): the tutorial that i am part of
            name(str): the name of the example
            header(str): the header/description of the example
            lines(list): the source code lines
        """
        self.tutorial=tutorial
        self.name=name
        self.header=header
        self.lines=lines
        
