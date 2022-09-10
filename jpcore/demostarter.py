"""
Created on 2022-09-22

@author: wf
"""
import asyncio
import importlib
import os
import sys
import traceback
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from examples.basedemo import Demo
from jpcore.justpy_app import JustpyDemoApp, JustpyServer


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
        script_dir = os.path.dirname(__file__)
        justpy_dir = f"{os.path.dirname(script_dir)}/examples"
        if self.debug:
            print(f"collecting examples from {justpy_dir}")
        pymodule_files = self.find_files(justpy_dir, ".py")
        self.demos = []
        self.servers = {}
        self.errors = {}
        for pymodule_file in pymodule_files:
            demo = JustpyDemoApp(pymodule_file)
            if demo.is_demo:
                self.demos.append(demo)
            else:
                if self.debug:
                    print(f"{pymodule_file} is not a demo")
        if self.debug:
            print(f"found {len(self.demos)} justpy demo python modules")

    async def start(self, baseport=11000, limit=None, use_gather: bool = False):
        """
        start the demos from the given baseport optionally limitting the number of demos

        Args:
            baseport(int): the port number to start from
            limit(int): the maximum number of demos to start (default: None)
            userGather(bool): if True try using gather
        """
        port = baseport
        server = None
        tasklist = []
        for i, demo in enumerate(self.demos):
            try:
                print(f"starting {i+1:3}:{demo}  ...")
                if server is None:
                    server = JustpyServer(mode=self.mode, port=port, debug=self.debug)
                else:
                    server = server.next_server()
                    self.servers[server.port] = server
                demo.port = server.port
                demo_module = importlib.import_module(demo.pymodule)
                demo.wp = getattr(demo_module, demo.endpoint)
                if use_gather:
                    tasklist.append(demo.start(server))
                else:
                    await demo.start(server)
            except Exception as ex:
                self.errors[i] = ex
                print(f"failed due to exception: {str(ex)}")
                if self.debug:
                    print(traceback.format_exc())
            if limit is not None and i + 1 >= limit:
                break
        if use_gather:
            demo_results = await asyncio.gather(*tasklist, return_exceptions=True)
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
        asyncio.run(demostarter.start(limit=args.limit))
    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        if args.debug:
            print(traceback.format_exc())
        return 2


if __name__ == "__main__":
    sys.exit(main())
