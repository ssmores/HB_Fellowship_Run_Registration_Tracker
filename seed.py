"""Utility file to seed run_registration_tracking from json file"""

from sqlalchemy import func
from model import User
from model import Race
from model import Tracked_Race
from model import Email_Transaction

from model import connect_to_db, db
from server import app

from datetime import datetime
import requests
import json


def load_initial_run():
    """Load some races from 'data.json' into database."""

    print "seed"

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

        event_distance = []
        for i in range(len(race['assetAttributes'])):
            if (race['assetAttributes'][i]['attribute']['attributeType'] 
                == "Distance (running)"):
                (event_distance.append(
                    race['assetAttributes'][i]['attribute']['attributeValue']))

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
                   event_distance=event_distance,
                   event_url=event_url)

        db.session.add(row)

    db.session.commit()
    f.close()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created:
    db.create_all()

    # Imports initial set of data
    load_initial_run()
