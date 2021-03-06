"""Models for race_tracking db."""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

class User(db.Model):
    """User of race tracking website."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_fname = db.Column(db.String(200), nullable=False)
    user_lname = db.Column(db.String(200), nullable=False)
    user_email = db.Column(db.String(600), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    tracked_races = db.relationship('Tracked_Race')

    def __repr__(self):
        """Provide user's first and last name."""

        return "<This is %s %s.>" % (self.user_fname, self.user_lname)

class Race(db.Model):
    """An individual race."""

    __tablename__ = 'races'

    race_id = db.Column(db.String(400), primary_key=True)
    event_name = db.Column(db.String(2000), nullable=False)
    # Start date is datetime, so recording the timezone offset and timezone DTS hours is needed.
    event_date = db.Column(db.DateTime, nullable=True)
    event_tzone_offset = db.Column(db.Integer, nullable=True)
    event_tzone_DST = db.Column(db.Integer, nullable=True)
    event_city = db.Column(db.String(200), nullable=True)
    event_state = db.Column(db.String(100), nullable=True)
    event_zipcode = db.Column(db.String(20), nullable=True)
    event_lat = db.Column(db.Float, nullable=True)
    event_lng = db.Column(db.Float, nullable=True)
    event_url = db.Column(db.String(1000), nullable=True)

    tracked_races = db.relationship('Tracked_Race')
    race_distances = db.relationship('Race_Distance')

    def __repr__(self):
        """Provides name, distance, and event date."""

        return "<Race name: %s, at %s.>" % (self.event_name, self.event_date)


class Tracked_Race(db.Model):
    """A tracked race/event from a user."""

    __tablename__ = 'tracked_races'

    tracked_race_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    race_id = db.Column(db.String(400), db.ForeignKey('races.race_id'))
    registered_status_indicator = db.Column(db.Boolean, default=False) 
    hotel_reserved_indicator = db.Column(db.Boolean, default=False)
    airfare_reserved_indicator = db.Column(db.Boolean, default=False)
    transportation_reserved_indicator = db.Column(db.Boolean, default=False)
    email_notification_start_date_at = db.Column(db.DateTime, nullable=True)
    email_notification_end_date_at = db.Column(db.DateTime, nullable=True)
    email_interval = db.Column(db.Integer, nullable=True)
    need_subsequent_email_indicator = db.Column(db.Boolean, default=False)

    user = db.relationship('User')
    race = db.relationship('Race')

    def __repr__(self):
        """Information on a tracked race."""

        return "<Registered for race: %s>" % (self.registered_status_indicator)


class Email_Transaction(db.Model):
    """Record of sent emails."""

    __tablename__ = 'email_transactions'

    transaction_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tracked_race_id = db.Column(db.Integer, db.ForeignKey('tracked_races.tracked_race_id'))
    email_date = db.Column(db.DateTime, nullable=True)
        
    # def __repr__(self):
    #     """Email transaction record."""

    #     return "<First email sent: %s.>" % (self.email_date)

class Distance_Type(db.Model):
    """A race distance."""

    __tablename__ = 'distance_types'

    distance_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    distance_length = db.Column(db.String(100), nullable=True, unique=True)

    race_distances  = db.relationship('Race_Distance')

    
    def __repr__(self):
        """Information on distance length."""

        return "<The %s distance length.>" % (self.distance_length)


class Race_Distance(db.Model):
    """Information on a race's distance(s)."""

    __tablename__ = 'race_distance'

    race_distance_id = db.Column(db.Integer, 
                                      autoincrement=True, 
                                      primary_key=True)
    race_id = db.Column(db.String(400), db.ForeignKey('races.race_id'))
    distance_type_id = db.Column(db.Integer, 
                                 db.ForeignKey('distance_types.distance_type_id'))

    races = db.relationship('Race')
    distance_types = db.relationship('Distance_Type')


def example_data():
    """Create sample data for testing."""

    test_user = User(user_fname='Curious',
                    user_lname='George',
                    user_email='curious@george.com',
                    password='abc123')
    test_race = Race(event_name='Test Race', 
                     event_date=2016-04-15, 
                     event_city='Oakland',
                     event_state='CA',
                     event_zipcode='94610')
    test_distance_5k = Distance_Type(distance_length='5k')
    test_distance_marathon = Distance_Type(distance_length='Marathon')

    db.session.add_all([test_user, test_race, test_distance_5k, test_distance_marathon])
    db.session.commit()


#########################################################################
# Helper functions

def connect_to_db(app, db_uri='postgresql:///run_registration_tracking'):
    """Connect to database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # app.config['SQLALCHEMY_ECHO'] = True #Remove this if I'm not debugging.
    db.app = app
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print "Connected to db"

 