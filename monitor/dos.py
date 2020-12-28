""" Service monitoring the DOSable endpoint

This service will report DOS status as it is monitored. Should the service go down, this will report that the service is
down. Fantastic!
"""
import requests

from monitor.base import Monitor, Health


TIMEOUT = 30 # 30 second timeout
LOCATION = "/dos"


class DOSMon(Monitor):
    """ Monitors the DOS service """

    def __init__(self, app):
        """ constructor """
        super().__init__(app)
        self.longest = 0

    @staticmethod
    def get_health(time):
        """ Get the current health of the service """
        if time < 10:
            return Health.HEALTHY
        elif time < 20:
            return Health.SICK
        else:
            return Health.DIEING

    def status(self):
        """ Reports the status of the request """
        try:
            # Prevent querying once it dead
            if self.longest > TIMEOUT:
                return "SERVICE FAILURE", Health.DEAD
            response = requests.get("http://localhost{}".format(LOCATION))
            time = response.elapsed.total_seconds()
            if time > self.longest:
                self.longest = time
            return "{}S - {}S".format(time, self.longest), self.get_health(time)
        except requests.exceptions.Timeout:
            return "SERVICE FAILURE", Health.DEAD

    def restart(self):
        self.longest = 0
        super().restart()