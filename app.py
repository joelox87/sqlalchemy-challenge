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
Station = Base.classes.station
Measurements = Base.classes.measurements

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
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > year_ago).\
        order_by(Measurement.date).all()







# Define main behavior
if __name__ == '__main__':
     app.run(debug=True) 



