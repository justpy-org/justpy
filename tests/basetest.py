"""
Created on 2021-08-19

@author: wf
"""

import getpass
from unittest import TestCase
import time
import os


class Basetest(TestCase):
    """
    base test case
    """

    def setUp(self, debug=False, profile=True):
        """
        setUp test environment
        """
        TestCase.setUp(self)
        self.debug = debug
        self.profile = profile
        msg = f"test {self._testMethodName}, debug={self.debug}"
        self.profiler = Profiler(msg, profile=self.profile)

    def tearDown(self):
        TestCase.tearDown(self)
        self.profiler.time()

    @staticmethod
    def inPublicCI():
        """
        are we running in a public Continuous Integration Environment?
        """
        publicCI = getpass.getuser() in ["travis", "runner"]
        jenkins = "JENKINS_HOME" in os.environ
        return publicCI or jenkins

    @staticmethod
    def isUser(name: str):
        """Checks if the system has the given name"""
        return getpass.getuser() == name


class Profiler:
    """
    simple profiler
    """

    def __init__(self, msg, profile=True):
        """
        construct me with the given msg and profile active flag

        Args:
            msg(str): the message to show if profiling is active
            profile(bool): True if messages should be shown
        """
        self.msg = msg
        self.profile = profile
        self.starttime = time.time()
        if profile:
            print(f"Starting {msg} ...")

    def time(self, extraMsg=""):
        """
        time the action and print if profile is active
        """
        elapsed = time.time() - self.starttime
        if self.profile:
            print(f"{self.msg}{extraMsg} took {elapsed:5.1f} s")
        return elapsed
