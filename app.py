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
# welcome
@app.route('/')
def welcome():
    return(
        f"Weclome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
          )

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
      
        "Available Routes:<br/> api/v1.0/precipitation")

@app.route("/api/v1.0/stations")
def stations():
    number_of_stations=session.query(stations.station).all()
    stations_list=session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs ():
    stations_list=session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()

@app.route("/api/v1.0/<start>")
def start_end():
    min_max_avg=session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.station=='USC00519281').all()



    session.close()