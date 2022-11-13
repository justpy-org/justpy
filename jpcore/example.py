'''
Created on 17.09.2022

@author: wf
'''
import os
import re
import datetime
from difflib import Differ
from jpcore.utilities import find_files

class ExampleSource:
    """
    source of an example - holding details such as the logo and url
    """
    
    def __init__(self,source_type:str="tutorial",description:str="",url:str=None,icon_size:int=32):
        """
        construct me with the given type and set the
        logo of the source type
        
        Args:
            source_type(str): e.g. tutorial/stackoverflow/issue
            url(str): the url
            icon_size(int): the size of the logo icon of the source_type, default: 32
        """
        self.source_type=source_type
        if source_type=="stackoverflow":
            # https://stackoverflow.design/brand/logo/
            self.logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Stack_Overflow_icon.svg/32px-Stack_Overflow_icon.svg.png"
            pass
        elif source_type=="github issue":
            # https://github.com/logos
            self.logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/32px-Octicons-mark-github.svg.png"
            pass
        else:
            # 32x32 pixel logo
            self.logo_url="https://elimintz.github.io/favicon.png"
            pass
        self.url=url
        self.description=description
        self.icon_size=icon_size
        
    @property
    def img_link(self):
        img_link=f"""<a href="{self.url}" target="_blank"><img src="{self.logo_url}" alt="{self.description}" title="{self.description}" style="width:{self.icon_size}px;height:{self.icon_size}px;"></a>"""
        return img_link
    
    def read_source(self,path:str):
        """
        read the source from the given path
        
        Args:
            path(str): the path to the module file
        """
        with open(path, "r") as source_file:
            self.source = source_file.read()
        self.lines=self.source.split("\n")
        
    @classmethod
    def of_path(cls,path:str):
        """
        derive a example source type from the given path
        
        Args:
            path(str): the path to the module file
            
        """
        issue_match=re.search("issue_([0-9]+)",path)
        if issue_match:
            issue_number=issue_match.group(1)
            issue_url=f"https://github.com/justpy-org/justpy/issues/{issue_number}"
            example_source=ExampleSource("github issue",description=f"github issue {issue_number}",url=issue_url)
        else:    
            stackoverflow_match=re.search("stackoverflow[/]q([0-9]+)",path)
            if stackoverflow_match:
                stackoverflow_number=stackoverflow_match.group(1)
                stackoverflow_url=f"https://stackoverflow.com/questions/{stackoverflow_number}"
                example_source=ExampleSource("stackoverflow",description=f"stackoverflow question {stackoverflow_number}",url=stackoverflow_url)
            else:
                example_source=ExampleSource()
        example_source.read_source(path)
        return example_source
    
    def same_as(self,other_source,debug:bool=False):
        """
        check whether this ExampleSource is the same as the other
        
        Args:
            other_source: the other source to compare with
            debug(bool): if True show debug information
        """     
        d=Differ()
        if debug:
            print(self)
            print(other_source)
        diff=d.compare(other_source.lines,self.lines)
        problems=[]
        for i,diff_line in enumerate(diff):
            if i==0:
                if not "# Justpy Tutorial demo" in diff_line:
                    problems.append("Justpy Tutorial demo comment in line 1 missing")
            elif diff_line.startswith("-"):
                if diff_line.startswith("- # generated by "):
                    pass
                elif diff_line.startswith("- jp.justpy("):
                    pass
                else:
                    problems.append(f"removed line {i+1}:{diff_line}")
            elif diff_line.startswith("+"):
                if diff_line.startswith("+ #"):
                    pass
                elif diff_line.startswith("+ # generated by demoapp"):
                    pass
                elif diff_line.startswith("+ from examples.basedemo import Demo"):
                    pass
                elif diff_line.startswith("+ Demo"):
                    pass
                elif diff_line.startswith("+ from  examples.basedemo import Demo"):
                    pass
                elif diff_line[2:].strip():
                    problems.append(f"added line {i+1}:{diff_line}")
            if debug:
                print(f"  {i+1:3}:{diff_line}")
        return problems
    
    def __str__(self):
        """
        return my string representation
        
        Returns:
            str: a text representation
        """
        text=f"{self.source_type}:{self.description}({len(self.lines)} lines)" 
        return text
        
class ExampleManager:
    """
    manages a collection of examples from a base directory
    """
    
    def __init__(self,base_path:str=None,debug:bool=False):
        """
        constructor
        
        Args:
            base_path(str): the base_path to use
            debug(bool): if True switch on debug mode
        """
        self.debug = debug
        self.script_dir = os.path.dirname(__file__)
        if base_path is None:
            base_path=os.path.dirname(self.script_dir)
        if base_path.endswith("/examples"):
            base_path=os.path.dirname(base_path)
        self.examples_dir = f"{base_path}/examples"
        self.example_json_file=f"{self.examples_dir}/examples.json"
        if self.debug:
            print(f"collecting examples from {self.examples_dir}")
        self.pymodule_files = find_files(self.examples_dir, ".py")
    
class Example:
    """
    an example
    """
    
    def __init__(self,example_source:ExampleSource,name:str,option:str=None,header:str="",lines:list=[]):
        """
        constructor
        
        Args:
            example_source(example_source): the source of this example e.g. tutorial/issue/stackoverflow Question
            name(str): the name of the example
            option(str): option
            header(str): the header/description of the example
            lines(list): the source code lines
        """
        self.example_source=example_source
        self.name=name
        self.option=option
        self.header=header
        self.example_source.lines=lines
        # optional back link to my tutorial
        self.tutorial=None
        
    def write_as_demo(self,target_path:str,verbose:bool=True):
        """
        write my source lines as a demo
           
        Args:
            target_path(str): the target path to extract the examples to
            verbose(bool): if True print progress messages
        """
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        timestamp=now.isoformat()
        src=self.example_source
        comment=f"""# Justpy Tutorial demo {self.name} 
# {src.description}       
#      
# generated by write_as_demo  at {timestamp} 
# 
# see {src.url}"""
        with open(target_path, 'w') as code:
            print(comment, file=code)
            for line in self.example_source.lines:
                if line.startswith("jp.justpy("):
                    args=line.replace("jp.justpy(","")
                    demo_start=f"""# initialize the demo
from examples.basedemo import Demo
Demo("{self.name}", {args}"""
                    print(demo_start,file=code)
                else:
                    print(line,file=code)
        if verbose:
            print(f"→{target_path}✅")        
        
    def __str__(self):
        """
        return my string representation
        
        Returns:
            str: a text representation
        """
        text=f"{self.name}({len(self.example_source.lines)} lines)"
        return text