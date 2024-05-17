#!/usr/bin/python3
"""
    a script that starts a Flask web application
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def index():
    """Returns Hello HBNB!"""
    return "Hello HBNB!"

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Returns HBNB"""
    return "HBNB"

@app.route("/c/<text>", strict_slashes=False)
def ctext(text):
    """Returns text"""
    text = text.replace('_', ' ')
    return "C " + text

@app.route("/python/<text>", strict_slashes=False)
def pytext(text="is cool"):
    """Returns text"""
    text = text.replace('_', ' ')
    return "Python " + text

@app.route("/number/<int:n>", strict_slashes=False)
def isnum(n):
    """Returns a number"""
    return '{} is a number'.format(n)

@app.route("/number_template/<int:n>", strict_slashes=False)
def isnumt(n):
    """Returns a template"""
    return render_template('5-number.html', n=n)


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
