"""Race Tracking App"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db
from model import (User, Race, Tracked_Race, Email_Transaction, 
                   Distance_Type, Race_Distance)

import os

key = os.environ['FLASK_SECRET']

app = Flask(__name__)
app.secret_key = key

@app.route('/')
def show_homepage():
    """Homepage for my race searching & logistics app."""

    return render_template("homepage.html")


@app.route('/login', methods=['GET'])
def login():
    """User login screen."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_screen():
    """User logs in."""

    user_id = request.form.get('user_id')
    password = request.form.get('password')

    # Query user table in database for user_id provided on screen.
    dbuser = User.query.filter(User.user_id == user_id).first()

    if dbuser:
        if dbuser.password == password:
            flash('Log in successful!')
            session['logged_in_user_id'] = user_id
            user_url_id = str(db.user_id)
            return render_template('/user/' + user_url_id)
        else:
            flash('Incorrect credentials. Please try again.')
            return redirect('/login')
    else:
        flash('No such user.')
        return redirect('/login')







if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(debug=True, host='0.0.0.0')