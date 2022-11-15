'''
Created on 2022-09-16

@author: wf
'''
from tests.basetest import Basetest
from jpcore.tutorial import TutorialManager
from jpcore.demostarter import Demostarter
from jpcore.example import ExampleSource

class TestTutorial(Basetest):
    """
    test synchronization between Tutorial and examples
    """
    
    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.tm=TutorialManager()
        self.ds=Demostarter()
    
    def check_tutorial(self,tm,ds,debug=False):
        """
        check the tutorial against the demo starter
        """
        if debug:
            print(f"found {len(tm.tutorials)} tutorials with {tm.total_examples} examples ({tm.total_lines} lines)")
        for i,tutorial in enumerate(tm.tutorials.values()):
            print (f"{i+1:3}:{tutorial.name} ({len(tutorial.lines):4} lines)")
            for j,example in enumerate(tutorial.examples.values()):
                print(f"  {j+1:2}:{example.name} ({example.header}) - {example.example_source.url}")
        header_missing=0
        html_used=0
        demo_missing=0
        for i,tutorial in enumerate(tm.tutorials.values()):
            for j,example in enumerate(tutorial.examples.values()):
                if example.option is not None:
                    if debug:
                        print(f"{tutorial.name} {example.name} option {example.option} used")
                        pass
                if not example.name in ds.demos_by_name:
                    demo_missing+=1
                    if debug:
                        print(f"❌ docs/{tutorial.name} {example.name} - demo missing")
                if example.header is None:
                    header_missing+=1
                    if debug:
                        print(f"❌ docs/{tutorial.name} {example.name} - header missing")
                elif "<" in example.header:
                    if debug:
                        print(f"❌ docs/{tutorial.name} {example.name} {example.header} - contains html markup")
                        html_used+=1
        if debug:
            print(f"{demo_missing} demos missing {header_missing} headers missing {html_used} x html used")
        self.assertEqual(0, header_missing + html_used, f"{demo_missing} demos missing; {header_missing} headers missing; {html_used} x html used")
        for demo in ds.demos:
            if not demo.name in tm.examples_by_name:
                if demo.example_source.source_type=="tutorial":
                    if debug:
                        print(f"❌ {demo.name} not linked to tutorial examples")
                
    def test_tutorial_manager(self):
        """
        test the tutorial manager
        """
        debug=True
        self.check_tutorial(self.tm, self.ds,debug=debug)
        if debug:
            print(f"found {len(self.tm.tutorials)} tutorial files")
        self.assertGreaterEqual(len(self.tm.tutorials), 70)
        
    def show_problems(self,problems):
        """
        show the given list of problems
        """ 
        for i,problem in enumerate(problems):
            print(f"  {i+1:2}:{problem}")
        
    def test_update_from_tutorial(self):
        """
        test updating an example from the tutorial source
        """
        debug=self.debug
        #debug=True
        #debug=False
        for example_name in ["stock_test2"]:
            target_path=f"/tmp/{example_name}.py"
            demo=self.ds.demos_by_name[example_name]
            tutorial_example=self.tm.examples_by_name[example_name]
            demo.update_from_tutorial_example(tutorial_example=tutorial_example,target_path=target_path)
            update_source=ExampleSource(description=f"test for {example_name}.py") 
            update_source.read_source(target_path)
            if debug:
                for i,line in enumerate(update_source.lines):
                    print (f"{i+1:3} {line}")
            problems=demo.same_as_tutorial(update_source,debug=debug) 
            if debug:
                self.show_problems(problems)       
            self.assertEqual(0,len(problems))
            
    def test_tutorial_extract(self):
        """
        test extracting tutorial code
        """
        self.tm.extract_all("/tmp/")
        # @TODO - check the diff of the extraction
        
    def test_tutorial_diff(self):
        """
        test the tutorial examples for matching with the tutorial source code
        """
        debug=True
        failed_checks=0
        for demo in self.ds.demos:
            if demo.name in self.tm.examples_by_name:
                tutorial_example=self.tm.examples_by_name[demo.name]
                tutorial_source=tutorial_example.example_source
                problems=demo.same_as_tutorial(tutorial_source,debug=False)
                if len(problems)>0:
                    failed_checks+=1
                    if debug:
                        print (demo.pymodule_file)
                        print (tutorial_example.tutorial)
                        print (tutorial_source.url)
                        self.show_problems(problems)
        if debug:
            print(f"❌ {failed_checks}/{len(self.ds.demos)} examples are not in sync with the tutorial content")
        #self.assertEqual(0,failed_checks)
        self.assertTrue(failed_checks<=16)