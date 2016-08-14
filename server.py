"""Race Tracking App"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db

import os

key = os.environ['FLASK_SECRET']

app = Flask(__name__)
app.secret_key = key

@app.route('/')
def show_homepage():
    """Homepage for my race searching & logistics app."""

    return render_template("homepage.html")







if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(debug=True, host='0.0.0.0')