"""Utility file to seed run_registration_tracking db from response file.

Data pulled from Active.com's API. The response will be turned into
a JSON object, which will be parsed accordingly.

The initial set of seed data will be races in Oakland, CA.
"""

# from sqlalchemy import func
from model import (Race, Distance_Type, Race_Distance)


from model import connect_to_db, db
from server import app

# from datetime import datetime
import requests
import json

import os


def run_initial_call():
    """Initial database seed will return results from Oakland, CA, for marathons."""
    key = os.environ['API_KEY']

    payload = {'query': 'marathon', 'city': 'Oakland', 
               'state': 'CA', 'radius': 50, 
               'api_key': key, 'sort': 'date_desc', 'exclude_children': 'true'}

    r = requests.get("http://api.amp.active.com/v2/search", params=payload)

    races = r.json()

    for i in range(len(races['results'])):
        race = races['results'][i]
        load_races(race)
        load_distance_types(race)
        load_race_distances(race)



def load_races(race):
    """Load some races from 'data.json' into database."""

    print "Seeding races."

    # f = open('seed_data/data.json')

    # for line in f:
    #     race = json.loads(line)
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

    # f.close()
    db.session.commit()


def load_distance_types(race):
    """Load some races from 'data.json' into databases."""

    print "Seeding distances."

    # race_distances = set()
    existing_distances = Distance_Type.query

    # f = open('seed_data/data.json')

    # for line in f:
    #     race = json.loads(line)
    for i in range(len(race['assetAttributes'])):
        if race['assetAttributes'][i]['attribute']['attributeType'] == "Distance (running)":
            length = race['assetAttributes'][i]['attribute']['attributeValue']
            if existing_distances.filter(Distance_Type.distance_length == length).first() is None:
                row = Distance_Type(distance_length=length)
                db.session.add(row)


    # f.close()

    # for race_distance in race_distances:
    #     row = Distance_Type(distance_length=race_distance)
    #     db.session.add(row)

    db.session.commit()


def load_race_distances(race):
    """Load the relationship between initial races and their distance(s)."""

    print "Seeding race distance types."

    race_distances = {}

    # f = open('seed_data/data.json')

    # for line in f:
    #     race = json.loads(line)
    race_id = race['assetGuid']
    race_distances[race_id] = []

    for i in range(len(race['assetAttributes'])):
        if race['assetAttributes'][i]['attribute']['attributeType'] == "Distance (running)":
            distance = race['assetAttributes'][i]['attribute']['attributeValue']
            race_distances[race_id].append(distance)

    # f.close()
            
    for race_id in race_distances:
        for distance in race_distances[race_id]:
            distance_type = Distance_Type.query.filter_by(distance_length=distance).one()
            distance_type_id = distance_type.distance_type_id

            row = Race_Distance(race_id=race_id,
                                distance_type_id=distance_type_id)
            db.session.add(row)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created:
    db.create_all()

    # Imports initial set of data
    run_initial_call()
    # load_races()
    # load_distance_types()
    # load_race_distances()


