""" Application used to monitor GWC hacking progress

This application is used to monitor the various hacking activities performed by GWC teams and report status of the
various activities. This reports to a webpage that presents the various content.
"""
import os
import shutil
import requests
from flask import Flask, jsonify, send_from_directory

# Services importations
from monitor.dos import DOSMon
from monitor.sql import SQLMon
from monitor.key import KeyMon


app = Flask(__name__)


# Monitor services
SERVICES = {"dos": DOSMon(app), "sql": SQLMon(app), "key": KeyMon(app)}
for key, service in SERVICES.items():
    service.setup()
    def get_view_function(key):
        """ Returns a view function """
        return lambda: "OK" if SERVICES[key].restart() is None else "OK2"
    app.route("/restart-{}".format(key), endpoint="restart-{}".format(key))(get_view_function(key))


# Status route used for reporting JSON status
@app.route('/status')
def status_json():
    """ Returns JSON formatted status """
    status_map = {key : service.current() for key, service in SERVICES.items()}
    return jsonify({
        "statuses": [{"key": key, "status": item[0], "health": str(item[1])} for key, item in status_map.items()]
    })


# For testing purposes
@app.route('/', defaults={'path': 'monitor.html'})
@app.route('/<path:path>')
def monitor_page(path):
    """ Function for returning normal files like a normal web server """
    return send_from_directory(os.path.join(os.path.dirname(__file__), "..", "static"), path)


if __name__ == '__main__':
    app.run(threaded=False, port=5000)