#!/usr/bin/python3
"""Starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """Displays a HTML page with a list of all State objects"""
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    return render_template('states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """Displays a HTML page with the cities of a given state"""
    state = storage.all(State).get('State.' + id)
    if state:
        cities = sorted(state.cities, key=lambda city: city.name)
        return render_template('9-states.html', state=state, cities=cities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
