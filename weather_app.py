import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template
import datetime as dt

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurement
Stations = Base.classes.station

weather_app = Flask(__name__)

@weather_app.route("/")
def Home_page():

    """Listing all available api routes."""
    
    return (
        f"All routes that are available:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        )


@weather_app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurements.date, Measurements.prcp).all()
    
    session.close()

    all_results = list(np.ravel(results))
    
    return jsonify(all_results)

@weather_app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Stations.station).all()

    session.close()
    
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@weather_app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date>"2016-08-23").all()

    session.close()
    
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

@weather_app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    """date = dt.datetime(int(start), 1, 1)"""
    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
    filter(Measurements.date >= start).all()

    session.close()
                            
    all_start = list(np.ravel(results)) 
                            
    return jsonify(all_start)
    
@weather_app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    """date = dt.datetime(int(start, end), 1, 1)"""

    if end < start:
        results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date <= start).filter(Measurements.date >= end).all()
    else:
        results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).filter(Measurements.date <= end).all()

    
    session.close()
    
    start_end = list(np.ravel(results))

    return jsonify(start_end)

if __name__ == '__main__':
    weather_app.run(debug=True)
