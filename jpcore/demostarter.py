"""
Created on 2022-09-22

@author: wf
"""
import json
import os
import sys
import traceback
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from examples.basedemo import Demo
from jpcore.example import ExampleManager
from jpcore.demoapp import JustpyDemoApp

class Demostarter(ExampleManager):
    """
    start justpy demos on different ports
    """

    def __init__(self, base_path:str=None,mode: str = None, debug: bool = False):
        """
        constructor

        Args:
            base_path(str): the base_path
            mode(str): the mode of the demo starter
            debug(bool): if True switch on debug mode
        """
        super().__init__(base_path=base_path,debug=debug)
        Demo.testmode = True
        self.mode = mode
        
        self.demos = []
        self.demos_by_name={}
        self.demos_by_source_file={}
        self.servers = {}
        self.errors = {}
        for pymodule_file in self.pymodule_files:
            demo = JustpyDemoApp(examples_dir=self.examples_dir,pymodule_file=pymodule_file,debug=debug)
            if demo.is_demo:
                self.demos.append(demo)
                self.demos_by_name[demo.name]=demo
                self.demos_by_source_file[demo.source_file]=demo
            else:
                if self.debug:
                    print(f"{pymodule_file} is not a demo")
        self.add_video_links()
        if self.debug:
            print(f"found {len(self.demos)} justpy demo python modules")
            
    def add_video_links(self):
        """
        add video links to the demos
        """
        with open(self.example_json_file) as json_file:
            # read in the example_json file
            example_json = json.load(json_file)
        if "examples" in example_json:
            for i, video_record in enumerate(example_json["examples"]):
                name=video_record.get("name",None)
                video_url=video_record.get("video_url",None)
                if name and video_url:
                    if name in self.demos_by_source_file:
                        demo=self.demos_by_source_file[name]
                    elif name in self.demos_by_name:
                        demo=self.demos_by_name[name]
                    demo.video_url=video_url
                    demo.issue=video_record.get("issue",None)
                    demo.fixed=video_record.get("fixed",None)
                else:
                    raise Exception(f"name or url missing for example #{i}")
            
    def as_list_of_dicts(self)->list:
        """
        convert me to a list of dicts for tabular display
        
        Returns:
            list: a list of records/dicts with information about the demos
        """
        lod=[]
        for i,demo in enumerate(self.demos):
            try_it_link=""
            demo_link=f"""<a href="/demo/{demo.name}" target="_blank">{demo.name}</a>"""   
            if demo.try_it_url:
                try_it_link=f"""<a href="{demo.try_it_url}" target="_blank">try {demo.name}</a>"""
            record={
                "#":i+1,
                "→": demo.example_source.img_link,
                "name": demo_link,
                "try it": try_it_link,
                "📹": "✅" if demo.video_url is not None else "❌",
                "source": demo.source_link,
                "status": demo.status
            }
            lod.append(record)
        return lod      

    def start(self,limit=None, use_gather: bool = False):
        """
        start the demos  optionally limitting the number of demos

        Args:
            limit(int): the maximum number of demos to start (default: None)
            userGather(bool): if True try using gather
        """
        import justpy as jp
        tasklist=[]
        jp.justpy(start_server=False)
        app=jp.app
        for i, demo in enumerate(self.demos):
            try:
                print(f"mounting {i+1:3}:{demo}  ...")
                if use_gather:
                    tasklist.append(demo.mount(app))
                else:
                    demo.mount(app)
            except Exception as ex:
                self.errors[i] = ex
                print(f"failed due to exception: {str(ex)}")
                if self.debug:
                    print(traceback.format_exc())
            if limit is not None and i + 1 >= limit:
                break
        server=jp.get_server()
        server.run()
        #if use_gather:
        #    demo_results = await asyncio.gather(*tasklist, return_exceptions=True)
        pass

    async def stop(self):
        """
        try stopping all servers
        """
        for server in list(self.servers.values()):
            if self.debug:
                print(f"stopping server at port {server.port} ...")
            await server.stop()
            self.servers.pop(server.port)

def main(argv=None):  # IGNORE:C0111
    """main program."""

    if argv is None:
        argv = sys.argv
    try:
        program_name = os.path.basename(sys.argv[0])
        parser = ArgumentParser(
            description="justpy demo module starter",
            formatter_class=RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            "-d", "--debug", dest="debug", action="store_true", help="show debug info"
        )
        parser.add_argument(
            "-m",
            "--mode",
            default=None,
            help="the server start mode process/direct or None for os specific (default: %(default)s)",
        )
        script_dir = os.path.dirname(__file__)
        parser.add_argument(
            "-p",
            "--path",
            default=os.path.dirname(script_dir),
            help="path to the examples (default: %(default)s)",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="limit the number of demos (default: %(default)s)",
        )

        args = parser.parse_args(argv[1:])
        demostarter = Demostarter(base_path=args.path,mode=args.mode, debug=args.debug)
        if args.debug:
            for demo in demostarter.demos:
                print(demo)
        demostarter.start(limit=args.limit)
    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        if args.debug:
            print(traceback.format_exc())
        return 2


if __name__ == "__main__":
    sys.exit(main())
