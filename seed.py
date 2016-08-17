"""Utility file to seed run_registration_tracking from json file"""

from sqlalchemy import func
from model import (User, Race, Tracked_Race, Email_Transaction, Distance_Type, Race_Distance_Type)


from model import connect_to_db, db
from server import app

from datetime import datetime
import requests
import json

def load_race_distances():
    """Load some races from 'data.json' into databases."""

    print "Seeding distances."

    race_distance = set()

    f = open('seed_data/data.json')

    for line in f:
        race = json.loads(line)
        for i in range(len(race['assetAttributes'])):
            if race['assetAttributes'][i]['attribute']['attributeType'] == "Distance (running)"
                race_distances.add(race['assetAttributes'][i]['attribute']['attributeValue'])

    f.close()

    for race_distance in race_distances:
        row = Distance_Type(distance_length=race_distance)
        db.session.add(row)

    db.session.commit()

def load_initial_races():
    """Load some races from 'data.json' into database."""

    print "Seeding races."

    f = open('seed_data/data.json')

    for line in f:
        race = json.loads(line)
        race_id = race['assetGuid']
        event_name = race['assetName']
        event_date = race['activityStartDate']
        event_tzone_offset = race['place']['timezoneOffset']
        event_tzone_DST = race['place']['timezoneDST']
        event_city = race['place']['cityName']
        event_state = race['place']['stateProvinceCode']
        event_zipcode = race['place']['postalCode']
        event_lat = race['place']['latitude']
        event_lng = race['place']['longitude']
        event_url = race['registrationUrlAdr']

        row = Race(race_id=race_id,
                   event_name=event_name,
                   event_date=event_date,
                   event_tzone_offset=event_tzone_offset,
                   event_tzone_DST=event_tzone_DST,
                   event_city=event_city,
                   event_state=event_state,
                   event_zipcode=event_zipcode,
                   event_lat=event_lat,
                   event_lng=event_lng,
                   event_url=event_url)

        db.session.add(row)

    f.close()
    db.session.commit()


def load_initial_race_distance_types():
    """Load the relationship between initial races and their distance(s)."""

    print "Seeding race distance types."




if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created:
    db.create_all()

    # Imports initial set of data
    load_initial_races()
    load_race_distances()


