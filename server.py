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
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_homepage():
    """Homepage for my race searching & logistics app."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def show_registration():
    """Page for new user registration."""

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def create_new_user():
    """Page for new user registration."""

    user_fname = request.form.get('user-first-name')
    user_lname = request.form.get('user-last-name')
    user_email = request.form.get('user-email')
    password = request.form.get('password')
    # confirmation_password = request.form.get('password-confirmation')

    # Queries user table in database for user_id provided by user.
    dbuser = User.query.filter(User.user_email == user_email).first()

    if dbuser:
        flash('This email address already taken.')
        return redirect('/register')
    else:
        user = User(user_fname=user_fname,
                    user_lname=user_lname,
                    user_email=user_email,
                    password=password)
        db.session.add(user)
        db.session.commit()
        flash('You have been created!')
        session['logged_in_user_email'] = user_email
        user_url_id = str(user.user_id)
        return render_template('/users/' + user_url_id)


@app.route('/login', methods=['GET'])
def login():
    """User login screen."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_screen():
    """User logs in."""

    user_email = request.form.get('user-email')
    password = request.form.get('password')

    # Query user table in database for user_id provided on screen.
    
    dbuser = User.query.filter(User.user_email == user_email).first()
    print dbuser.user_id

    if dbuser:
        if dbuser.password == password:
            flash('Log in successful!')
            session['logged_in_user_email'] = user_email

            user_url_id = dbuser.user_id
            session['user_id'] = user_url_id
            user_url_id = str(dbuser.user_id)
            return redirect('/users/' + user_url_id)
        else:
            flash('Incorrect credentials. Please try again.')
            return redirect('/login')
    else:
        flash('No such user.')
        return redirect('/login')


@app.route('/users/<user_id>')
def show_user_info(user_id):
    """Show user information."""

    user_details = User.query.filter(User.user_id == user_id).one()
    user_fname = user_details.user_fname
    user_lname = user_details.user_lname
    user_email = user_details.user_email
    tracked_races = user_details.tracked_races
    print tracked_races

    return render_template('user_detail.html',
                           user_fname=user_fname,
                           user_lname=user_lname,
                           user_email=user_email,
                           user_id=user_id,
                           tracked_races=tracked_races)


@app.route('/tracked_race_logistics/<race_id>')
def show_tracked_race_details(race_id):
    """Show details of race and travel logistics for user's specified race."""

    user_id = session['user_id']

    tracked_race = Tracked_Race.query.filter(
        Tracked_Race.race_id == race_id, 
        Tracked_Race.user_id == user_id ).one()

    return render_template('tracked_race_logistics.html',
                           tracked_race=tracked_race)


@app.route('/search_results', methods=['GET'])
def show_races():
    """Show race results based on search page parameters."""

    city = request.args.get('city')
    state = request.args.get('state')
    zipcode = request.args.get('zipcode')
    distance = request.args.get('racedistance')


    print city, state, zipcode, distance

    q = Race.query
    results = q.filter(Race.event_city == city).all()

    return render_template ('search_results.html',
                            results=results)


@app.route('/search_results/<race_id>')
def show_race_details(race_id):
    """Show details of specific race result."""

    race_detail = Race.query.filter(Race.race_id == race_id).one()
    event_name = race_detail.event_name
    event_city = race_detail.event_city
    event_state= race_detail.event_state
    event_zipcode = race_detail.event_zipcode

    event_date = race_detail.event_date
    event_tzone_DST = race_detail.event_tzone_DST
    event_tzone_offset = race_detail.event_tzone_offset

    return render_template('race_detail.html', 
                           event_name=event_name,
                           event_city=event_city,
                           event_state=event_state,
                           event_zipcode=event_zipcode,
                           event_date=event_date,
                           event_tzone_DST=event_tzone_DST,
                           event_tzone_offset=event_tzone_offset,
                           race_id=race_id)


@app.route('/add_race/<race_id>')
def add_tracked_race(race_id):
    """Adding tracked race."""

    race = race_id
    user = session['user_id']

    q = Tracked_Race.query
    verify_race = q.filter(Tracked_Race.user_id == user, Tracked_Race.race_id == race).first() 

    if verify_race == None:
        tracked_race = Tracked_Race(user_id=user, race_id=race)
        db.session.add(tracked_race)
        db.session.commit()
        flash("Race added! What about these other things?")
        return render_template('tracked_race_logistics.html',
                               tracked_race=tracked_race) 
    else:
        flash("You are already tracking this race!")
        return redirect('tracked_race_logistics.html')


@app.route('/logout')
def log_out():
    """Log out page."""

    session.pop('logged_in_user_email', None)
    session.pop('user_id', None)
    flash("You are now logged out.")
    return redirect('/login')



if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(debug=True, host='0.0.0.0')