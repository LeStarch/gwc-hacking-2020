""" app.py:

Flask app that returns a message after a fixed amount of time. It is deliberately slow, to allow for an opportunity to
DOS the server (for learning purposes). DO NOT uses this code as a basis for a real server. It likely will not go well
as it is designed to fail.
"""
import os
import time
from flask import Flask, send_from_directory


RESPONSE_TIME=0.200
app = Flask(__name__)


@app.route('/dos')
@app.route('/dos.html')
def dos_service():
    time.sleep(RESPONSE_TIME)
    return send_from_directory(os.path.join(os.path.dirname(__file__), "..", "static"), "dos.html")


if __name__ == '__main__':
    app.run(threaded=False, port=5001)
