from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,inspect, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
measurement= Base.classes.measurement
stations=Base.classes.station
# Create our session (link) from Python to the DB
session= Session(engine)
# inspector=inspect(engine)
station= engine.execute("SELECT* FROM station")
station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation as json"""
    station= engine.execute("SELECT* FROM station")
    previous_year=dt.date(2017, 8 ,23)- dt.timedelta(days=365)
    scores=session.query(measurement.date, measurement.prcp).filter(measurement.date>previous_year).all()
    print (scores)
    return str (scores) 
    # return scores[0]
@app.route("/")
def welcome():
    return (
      
        "Available Routes:<br/> api/v1.0/precipitation"
       
    )


