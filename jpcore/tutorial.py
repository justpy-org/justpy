'''
Created on 2022-09-16

@author: wf
'''
import os
import sys
import re
from jpcore.utilities import find_files
from jpcore.example import Example, ExampleSource
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import traceback

class TutorialManager:
    """
    justpy tutorial
    """
    
    def __init__(self,docs_dir:str=None,debug:bool=False):
        """
        constructor
        
        Args:
            docs_dir(str): the path from which to read the tutorial files
            debug(bool): if True switch debugging on
        """
        self.debug=debug
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
        if self.debug:
            print(f"{docs_dir} contains {len(self.tutorials)} tutorials with {self.total_examples} examples")
            pass
                
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
        for i,example_name in enumerate(sorted_example_names):
            prefix=f"  {i+1:3}:"
            self.extract_example(example_name,target_path,prefix=prefix,verbose=verbose)
        
    def extract_example(self,example_name:str,target_path:str,prefix:str="",verbose:bool=True):
        """
        extract the example with the given name to the given base_path
        
        Args:
            example_name(str): the name of the example to extract
            target_path(str): the path to extract the example to
            prefix(str): a prefix for the message to display
            verbose(bool): if True show details of the extraction process
        """
        if not example_name in self.examples:
            raise Exception(f"{example_name} is not part of tutorial {self}")   
        example=self.examples[example_name]
        if not target_path.endswith("/"):
            target_path+="/"
        base_path=f"{target_path}{self.tutorial_path}"
        os.makedirs(base_path, exist_ok=True)
        source_target_path=f"{base_path}/{example_name}.py"
        if verbose:
            print(f"{prefix}{example_name}:{example}",end="")
        header=f"""# see {self.github_url}
"""
        example.write_as_demo(source_target_path,header=header,verbose=verbose)
                    
    def __str__(self):
        """
        return my text representation
        
        Returns:
            str: a text representation of me
        """
        text=self.path
        return text
    
def error(self,msg:str):
    """
    print the given error message and exit
    
    Args:
        msg(str): the error message to print
    """
    print(msg,file=sys.stderr)
    sys.exit(1)
    
def main(argv=None):  # IGNORE:C0111
    """main program."""

    if argv is None:
        argv = sys.argv
    try:
        program_name = os.path.basename(sys.argv[0])
        script_dir = os.path.dirname(__file__)
        base_dir=os.path.dirname(script_dir)
        # os.getcwd()
        parser = ArgumentParser(
            description="Tutorial Manager",
            formatter_class=RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            "-d", "--debug", dest="debug", action="store_true", help="show debug info"
        )
        parser.add_argument(
            "-dp",
            "--docs_path",
            default=f"{base_dir}/docs",
            help="path to the docs directory (default: %(default)s)",
        )
        parser.add_argument(
            "-ep",
            "--examples_path",
            default=f"{base_dir}/examples",
            help="path to the examples directory (default: %(default)s)",
        )
        parser.add_argument(
            "-ex",
            "--extract",
            default=None,
            help="name of example to extract (default: %(default)s)",
        )
        args = parser.parse_args(argv[1:])
        tm=TutorialManager(docs_dir=args.docs_path,debug=args.debug)
        if args.extract:
            example_name=args.extract
            if example_name in tm.examples_by_name:
                target_path=f"{args.examples_path}"
                example=tm.examples_by_name[example_name]
                if example.tutorial is not None:
                    prefix=f"extracting source code for "
                    example.tutorial.extract_example(example_name,target_path,prefix=prefix)
                else:
                    error(f" found {example_name} but not tutorial entry for it ❌")
                    print(f"found ")
            else:
                error(f"tutorial does not contain the example {example_name} ❌",file=sys.stderr)
        else:
            parser.print_help(sys.stderr)
            error("no valid option given")
    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        if args.debug:
            print(traceback.format_exc())
        return 2    
    
if __name__ == "__main__":
    sys.exit(main())