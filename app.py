# Import Dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Reflect Database into ORM classes
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo = False)
Base = automap_base()
Base.prepare(engine, reflect = True)

# Save table references
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session between Python and database
session = Session(engine)

#Create an app
app = Flask(__name__)

#Define static routes
@app.route("/")
def home():
    """Here is a list of all availables API routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>") 

@app.route("/api/v1.0/precipitation")    
def precipitation():
    # Query last 12 months of precipitation data 
    year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)
    prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > year_ago).\
        order_by(Measurement.date).all()

# Create a list of dicts with `date` and `prcp` as the keys and values
    prcp_total = []
    for i in prcp:
        row = {}
        row["date"] = i[0]
        row["prcp"] = i[1]
        prcp_total.append(row)
    return jsonify(prcp_total)

@app.route("/api/v1.0/stations")
# Return a JSON list of stations from the dataset
def stations():
    station_results = session.query(Station.station).all()
    all_stations = list(np.ravel(station_results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
# Query the dates and temperature observations of the most active station for the last year of data
def tobs():
    temps = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').all()
    tobs_list = []
    for i in temps:
        tobs_dict = {}
        tobs_dict["date"] = i[1]
        tobs_dict["tobs"] = i[2]
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    start_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    start_tobs = []
    for min,avg,max in start_query:
        start_dict = {}
        start_dict["Min"] = min
        start_dict["Max"] = max
        start_dict["Average"] = avg
        
        start_tobs.append(start_dict)
    return jsonify(start_tobs)

if __name__ == '__main__':
    app.run(debug=True)