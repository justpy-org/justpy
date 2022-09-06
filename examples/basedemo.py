"""
Created on 2022-09-07

@author: wf
"""
import argparse
import socket
import typing


class Demo(object):
    """
    Base class for justpy demos to allow selecting host and port from commandline
    """

    testmode = False

    def __init__(self, name: str, wp: typing.Callable, **kwargs):
        """
        Constructor

        Args:
            name(str): the name of the demo
            host(int): the port to runt he demo at (defaut:8000)
            wp(callable): the webpage callback
            **kwargs: further keyword arguments
        """
        # make sure Demo code may be tested without automatically starting
        if Demo.testmode:
            return
        parser = argparse.ArgumentParser(description=name)
        parser.add_argument("--host", default=socket.getfqdn())
        parser.add_argument("--port", type=int, default=8000)
        args = parser.parse_args()
        import justpy as jp

        jp.justpy(wp, host=args.host, port=args.port, **kwargs)
