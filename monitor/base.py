""" Contains the base monitor that controls the basic monitor functions """
from enum import Enum
from abc import ABC, abstractmethod
from threading import Thread


class Health(Enum):
    """ Health of status """
    NONE = 0
    HEALTHY = 1
    SICK = 2
    DIEING = 3
    DEAD = 4


class Monitor(object):
    """ Base monitor object that allows for starting/restarting thread """

    def __init__(self, app):
        """ consturctor """
        self.app = app
        self.running = False
        self.thread = None
        self.latest = "STARTING", Health.NONE

    def setup(self):
        """ Setup the thread for running """
        assert self.thread is None and self.running is False, "Cannot setup without previous shutdown"
        self.latest = "STARTING", Health.NONE
        self.running = True
        self.thread = Thread(target=self.loop)
        self.thread.start()

    def loop(self):
        """ Run the threading loop """
        latest = "STARTING", Health.NONE
        while self.running:
            self.latest = latest # Allow breaking the loop before updating status
            latest = self.status()

    @abstractmethod
    def status(self):
        """ Get the status of the request """
        pass

    def current(self):
        """ Get the latest status from the system """
        return self.latest

    def teardown(self):
        """ Teardown this thread in order to restart """
        self.running = False
        self.latest = "STOPPING", Health.NONE
        self.thread.join()
        self.thread = None

    def restart(self):
        """ Restarts this thread """
        self.teardown()
        self.setup()