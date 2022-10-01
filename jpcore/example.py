'''
Created on 17.09.2022

@author: wf
'''
import re

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
    
    def __str__(self):
        """
        return my string representation
        
        Returns:
            str: a text representation
        """
        text=f"{self.source_type}:{self.description}({len(self.lines)} lines)" 
        return text
        
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
        
    def __str__(self):
        """
        return my string representation
        
        Returns:
            str: a text representation
        """
        text=f"{self.name}"
        return text