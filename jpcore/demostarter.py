"""
Created on 2022-09-22

@author: wf
"""
import asyncio
import json
import os
import sys
import traceback
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from examples.basedemo import Demo
from jpcore.justpy_app import JustpyDemoApp
import justpy as jp

class Demostarter:
    """
    start justpy demos on different ports
    """

    def __init__(self, mode: str = None, debug: bool = False):
        """
        constructor

        Args:
            debug(bool): if True switch on debug mode
        """
        Demo.testmode = True
        self.debug = debug
        self.mode = mode
        self.script_dir = os.path.dirname(__file__)
        self.justpy_dir = f"{os.path.dirname(self.script_dir)}/examples"
        self.video_json_file=f"{os.path.dirname(self.script_dir)}/tutorial/videos.json"
        if self.debug:
            print(f"collecting examples from {self.justpy_dir}")
        pymodule_files = self.find_files(self.justpy_dir, ".py")
        self.demos = []
        self.demos_by_name={}
        self.demos_by_source_file={}
        self.servers = {}
        self.errors = {}
        for pymodule_file in pymodule_files:
            demo = JustpyDemoApp(examples_dir=self.justpy_dir,pymodule_file=pymodule_file,debug=debug)
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
        with open(self.video_json_file) as json_file:
            video_json = json.load(json_file)
            if "videos" in video_json:
                for i,video_record in enumerate(video_json["videos"]):
                    name=video_record.get("name",None)
                    url=video_record.get("url",None)
                    if name and url:
                        if name in self.demos_by_source_file:
                            demo=self.demos_by_source_file[name]
                            demo.video_url=url
                        elif name in self.demos_by_name:
                            demo=self.demos_by_name[name]
                            demo.video_url=url
                    else:
                        raise Exception(f"name or url missing for video #{i}")
                    
            pass
        
            
    def as_list_of_dicts(self,video_size=128)->list:
        """
        convert me to a list of dicts for tabular display
        
        Returns:
            list: a list of records/dicts with information about the demos
        """
        lod=[]
        for i,demo in enumerate(self.demos):
            video_link=""
            try_it_link=""
            if demo.video_url:
                video_link=f"""<a href="{demo.video_url}"><img src="{demo.video_url}" alt="video for {demo.name}" style="width:{video_size}px;height:{video_size}px;"></a>"""
            demo_link=f"""<a href="/demo/{demo.name}" target="_blank">{demo.name}</a>"""   
            if demo.try_it_url:
                try_it_link=f"""<a href="{demo.try_it_url}" target="_blank">try {demo.name}</a>"""
            record={
                "#":i+1,
                "name": demo_link,
                "try it": try_it_link,
                "video": video_link,
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

    def find_files(self, path: str, ext: str) -> list:
        """
        find files with the given extension in the given path

        Args:
            path(str): the path to start with
            ext(str): the extension to search for

        Returns:
            list: a list of files found
        """
        foundFiles = []
        for root, _dirs, files in os.walk(path, topdown=False):
            for name in files:
                if name.endswith(ext):
                    filepath = os.path.join(root, name)
                    foundFiles.append(filepath)
        return foundFiles


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
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="limit the number of demos (default: %(default)s)",
        )

        args = parser.parse_args(argv[1:])
        demostarter = Demostarter(mode=args.mode, debug=args.debug)
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
