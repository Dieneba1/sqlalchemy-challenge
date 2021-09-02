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

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route('/')
def welcome():
    return(
        # f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
          )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session= Session(engine)
    """Return precipitation as json"""
    # station= engine.execute("SELECT* FROM station")
    previous_year=dt.date(2017, 8 ,23)- dt.timedelta(days=365)
    scores=session.query(measurement.date, measurement.prcp).filter(measurement.date>previous_year).all()
    results=[]
    for score in scores:
        values={}
        values[score[0]]=score[1]
        results.append(values)
    session.close()
    print (scores)
    return jsonify (results) 
   

@app.route("/api/v1.0/stations")
def stations_number():
    session= Session(engine)
    number_of_stations=session.query(stations.station).all()
    stations_result=[]
    for number_of_station in number_of_stations:
        stations_result.append(number_of_station[0])
    session.close()
    return jsonify( stations_result)


@app.route("/api/v1.0/tobs")
def tobs ():
    session= Session(engine)
    previous_year=dt.date(2017, 8 ,23)- dt.timedelta(days=365)
    stations_lists=session.query(measurement.tobs).filter(measurement.date>=previous_year).filter(measurement.station=='USC00519281').all()
    station_list_result=[]
    for station_list in stations_lists:
        station_list_result.append(station_list[0])
    session.close()
    return jsonify(station_list_result)

@app.route("/api/v1.0/<start>")
def start(start):
    session= Session(engine)
    min_max_avg=session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date>=start).all()
    session.close()
    min_max_avg_result=[]
    min_max_avg_result.append(min_max_avg[0][0])
    min_max_avg_result.append(min_max_avg[0][1])
    min_max_avg_result.append(min_max_avg[0][2])
    return jsonify(min_max_avg_result)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session= Session(engine)
    min_max_avg=session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date>=start).filter(measurement.date<=end).all()
    session.close()
    min_max_avg_result=[]
    min_max_avg_result.append(min_max_avg[0][0])
    min_max_avg_result.append(min_max_avg[0][1])
    min_max_avg_result.append(min_max_avg[0][2])
    return jsonify(min_max_avg_result)
if __name__ == '__main__':
    app.run()