'''
Created on 2022-09-16

@author: wf
'''
from tests.basetest import Basetest
from jpcore.tutorial import TutorialManager
from jpcore.demostarter import Demostarter

class TestTutorial(Basetest):
    """
    test synchronization between Tutorial and examples
    """
    
    def check_tutorial(self,tm,ds,debug=False):
        """
        check the tutorial against the demo starter
        """
        if debug:
            print(f"found {len(tm.tutorials)} tutorials with {tm.total_examples} examples ({tm.total_lines} lines)")
        for i,tutorial in enumerate(tm.tutorials.values()):
            print (f"{i+1:3}:{tutorial.name} ({len(tutorial.lines):4} lines)")
            for j,example in enumerate(tutorial.examples.values()):
                print (f"  {j+1:2}:{example.name} ({example.header}) - {example.example_source.url}")
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
        self.assertEqual(0,header_missing+html_used)
        for demo in ds.demos:
            if not demo.name in tm.examples_by_name:
                if demo.example_source.source_type=="tutorial":
                    if debug:
                        print(f"❌ {demo.name} not linked to tutorial examples")
                
    def test_tutorial_manager(self):
        """
        test the tutorial manager
        """
        tm=TutorialManager()
        ds=Demostarter()
        debug=True
        self.check_tutorial(tm,ds,debug=debug)
        if debug:
            print(f"found {len(tm.tutorials)} tutorial files")
        self.assertTrue(len(tm.tutorials)>=70)