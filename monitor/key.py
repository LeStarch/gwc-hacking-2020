""" Service monitoring the DOSable endpoint

This service will report DOS status as it is monitored. Should the service go down, this will report that the service is
down. Fantastic!
"""
from flask import request
from monitor.base import Monitor, Health

CORRECT = {
    "facebook.com": ("thementor@awesome.mentorthe.com", "IB4theMentor$facebook"),
    "twitter.com": ("thementor8455@gmail.com", "IB4theMentor$twitter"),
    "gmail.com": ("thementor8455@gmail.com", "IB4theMentor$gmail2020"),
    "System Admin": (None, "IB4theMentor$")
}
SINGLETON = None

class KeyMon(Monitor):
    """ Monitors the KeyLogger activity """

    def __init__(self, app):
        """ Initialize the keymonitor program """
        global SINGLETON
        app.route("/key", methods=["POST"])(self.check)
        self.done = {key : False for key in CORRECT.keys()}
        SINGLETON = self
        super().__init__(app)

    def restart(self):
        """ Reset the service"""
        self.done = {key : False for key in CORRECT.keys()}
        super().restart()

    def status(self):
        """ Reports the status of the request """
        count = len([item for item in self.done.values() if item])
        return "{} passwords extracted".format(count), Health(min(count + 1, Health.DEAD.value))

    @staticmethod
    def check():
        """ SQL service, poorly implemented"""
        service_string = request.form.get("service", "")
        user_string = request.form.get("user", "n/a")
        pass_string = request.form.get("password", "")

        correct = CORRECT.get(service_string, ("ahhh<WE*#&$^@MM#&$hhh", None))
        filled_user = "n/a" if correct[0] is None else user_string
        if correct[0] is None and correct[1] == pass_string or correct == (user_string, pass_string):
            SINGLETON.done[service_string] = True
            return "Successful login to {} with user {}".format(service_string, filled_user)
        return "Failed to login to {} with user {}".format(service_string, filled_user)
