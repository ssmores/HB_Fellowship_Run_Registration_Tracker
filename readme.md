Run Registration Tracker
--------------------------


**Description**

Find running races and track your registration status, and travel logistics status (airfare, hotel, transportation) for each race.  Email yourself about the tracked race as well. 

Learn more about the developer on [LinkedIn](www.linkedin.com/in/stefaniemoy). 

**How it works**

Data is seeded from data returned from an API request using Active.com's API.  


### Technology Stack

* Back-End: Python, Flask
* Front-End: JavaScript, AJAX, jQuery, Bootstrap, HTML, CSS, Jinja
* Database: PostgreSQL, SQLAlchemy
* APIs: Active.com 


### How to run locally

Register at [Active.com's website](http://developer.active.com/docs/read/v2_Activity_API_Search). 


Create a virtual environment 

```
>>> virtualenv env
>>> source env/bin/activate
```

Install the dependencies

```
>>> pip install -r requirements.txt
```