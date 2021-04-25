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
    for result in prcp:
        row = {}
        row["date"] = prcp[0]
        row["prcp"] = prcp[1]
        prcp_total.append(row)
    return jsonify(prcp_total)

# Define main behavior
if __name__ == '__main__':
     app.run(debug=True) 



