'''
Created on 2022-09-16

@author: wf
'''
import os
import re
from jpcore.utilities import find_files
from jpcore.example import Example, ExampleSource

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
        self.examples_by_name={}
        self.tutorial_files = find_files(self.docs_dir, ".md")
        for tutorial_file_path in self.tutorial_files:
            tutorial=Tutorial(docs_dir,tutorial_file_path)
            self.tutorials[tutorial.name]=tutorial
            self.total_lines+=len(tutorial.lines)
            self.total_examples+=len(tutorial.examples)
            for example in tutorial.examples.values():
                if example.name in self.examples_by_name:
                    duplicate_example=self.examples_by_name[example.name]
                    raise Exception(f"duplicate example name '{example.name}' {example.tutorial.name} and {duplicate_example.tutorial.name}")
                self.examples_by_name[example.name]=example
                
    def extract_all(self,target_path:str="/tmp",verbose:bool=True):
        """
        extract demo source code for all tutorial examples
        
        Args:
            target_path(str): the target path to extract the examples to
            verbose(bool): if True print progress messages
        """
        if verbose:
            print(f"extracting demo source code for {len(self.tutorials)} tutorials with {len(self.examples_by_name)} examples")
        sorted_tutorial_names=sorted(self.tutorials.keys())
        for i,tutorial_name in enumerate(sorted_tutorial_names):
            tutorial=self.tutorials[tutorial_name]
            if verbose:
                print(f"{i+1:3}:{tutorial_name}:{tutorial}")   
            tutorial.extract_examples(target_path,verbose)
        
        
class Tutorial():
    """
    a single tutorial file
    """
    
    def __init__(self,docs_dir:str,path:str):
        """
        construct me
        
        Args:
            docs_dir(str): the path to the tutorials
            path(str): the full path
        """
        self.examples={}
        self.path=path
        self.docs_dir=docs_dir
        self.name=path.replace(docs_dir+"/","")
        self.tutorial_path=self.name.replace(".md","")
        self.tutorial_url=f"https://justpy.io/{self.tutorial_path}"
        self.github_url=f"https://github.com/justpy-org/justpy/blob/master/docs/{self.name}"
        with open(self.path, "r") as markup_file:
            self.markup = markup_file.read()
        self.lines=self.markup.split("\n")
        header=None
        python_code=[]
        in_python_code=False
        for line in self.lines:
            if line.startswith("```python"):
                in_python_code=True
                python_code=[]
                continue
            if line.startswith("```"):
                in_python_code=False
                continue
            if not in_python_code:
                header_match= re.search("^#+\s*(.*)",line)
                if header_match:
                    header=header_match.group(1)
                    header=header.strip()
                    pass
            else:
                python_code.append(line)
                justpy_match = re.search(
                    """^(jp[.])?justpy[(]([a-zA-Z_0-9]*)([,]\s*(.*))?[)]([#].*)?""", line
                )
                if justpy_match:
                    example_name = justpy_match.group(2)
                    example_option=justpy_match.group(4)
                    example_comment=justpy_match.group(5)
                    if not example_name:
                        example_name=example_comment
                        pass
                    example_source=ExampleSource("tutorial")
                    example_source.lines=python_code
                    if header is not None:
                        # https://stackoverflow.com/questions/72536973/how-are-github-markdown-anchor-links-constructed
                        lower=header.strip().lower().replace(" ","-")
                        anchor=""
                        for c in lower:
                            if c.isalnum() or c in "-_":
                                anchor+=c
                        example_source.url=f"{self.tutorial_url}#{anchor}"
                        example_source.anchor=anchor
                        example_source.description=header
                    example=Example(example_source,name=example_name,option=example_option,header=header,lines=python_code)
                    example.tutorial=self
                    self.examples[example.name]=example
                    header=None
                    python_code=[]
                    in_python_code=False
                    
    def extract_examples(self,target_path:str="/tmp",verbose:bool=True):
        """
        extract demo source code for all my tutorial examples
        
        Args:
            target_path(str): the target path to extract the examples to
            verbose(bool): if True print progress messages
        """
        sorted_example_names=sorted(self.examples)
        base_path=f"{target_path}{self.tutorial_path}"
        os.makedirs(base_path, exist_ok=True)
        for i,example_name in enumerate(sorted_example_names):
            example=self.examples[example_name]
            source_target_path=f"{base_path}/{example_name}.py"
            if verbose:
                print(f"  {i+1:3}:{example_name}:{example}",end="")
            example.write_as_demo(source_target_path,verbose)
                    
    def __str__(self):
        """
        return my text representation
        
        Returns:
            str: a text representation of me
        """
        text=self.path
        return text