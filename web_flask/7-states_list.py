#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
from models import *
from models import storage

app = Flask(__name__)

@app.route("/states_list", strict_slashes=False)
def states():
    """ Returns a template with states listed alphabetically"""
    states = sorted(storage.all("State").values()), key = lambda x: x.name)
    return render_template("7-states_list.html")

@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session."""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
