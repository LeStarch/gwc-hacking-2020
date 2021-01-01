""" Service monitoring the DOSable endpoint

This service will report DOS status as it is monitored. Should the service go down, this will report that the service is
down. Fantastic!
"""
import requests
import time
from monitor.base import Monitor, Health


TIMEOUT = 30 # 30 second timeout
LOCATION = "/dos"


class DOSMon(Monitor):
    """ Monitors the DOS service """

    def __init__(self, app):
        """ constructor """
        super().__init__(app)
        self.longest = 0
        self.start = None

    @staticmethod
    def get_health(time):
        """ Get the current health of the service """
        if time < 10:
            return Health.HEALTHY
        elif time < 20:
            return Health.SICK
        else:
            return Health.DIEING

    def current(self):
        """ Override current for better understanding of timeing """
        current_time = time.time() - self.start
        longest = max(self.longest, current_time)
        if longest < TIMEOUT:
            return "Longest delay: {}S".format(longest, self.longest), self.get_health(longest)
        return "Service failed", Health.DEAD

    def status(self):
        """ Reports the status of the request """
        try:
            # Prevent querying once it dead
            self.start = time.time()
            response = requests.get("http://localhost{}".format(LOCATION), timeout=TIMEOUT)
            time_real = response.elapsed.total_seconds()
            if time_real > self.longest:
                self.longest = time_real
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            self.longest = TIMEOUT
        return "Unused", Health.NONE

    def restart(self):
        self.longest = 0
        super().restart()