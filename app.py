import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime
from datetime import timedelta
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table, bringing in measurement and station tables from sqlite database
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
#Home page creation
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")

#precipitation page
@app.route("/api/v1.0/precipitation")
def precipitation():


    #Query the date and preciptation from last year
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > "2016-08-19").all()

    # Convert above query to JSON
    precip_list = []
    for x in precipitation_data:
        precip_dict = {}
        precip_dict[x[0]] = x[1]
        precip_list.append(precip_dict)

    #session,close()

    return jsonify(precip_list)

#stations page
@app.route("/api/v1.0/stations")
def stations():
    #Query the station data
    stations_data = session.query(Station).all()
    station_list = []
    #looping hawaii station csv data
    for x in stations_data:
        stations_dict = {}
        stations_dict['station'] = x.station
        stations_dict['name']=x.name
        stations_dict['latitude']=x.latitude
        stations_dict['longitude']=x.longitude
        stations_dict['elevation']=x.elevation
        station_list.append(stations_dict)

    return jsonify(station_list)

#temperature page
@app.route("/api/v1.0/tobs")
def temperature():
    #Query the temperature/dates for active station
    temperature_station_data = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >='2016-08-19').all()
    temp_list = []
    #looping active station tobs
    for x in temperature_station_data:
        temp_dict = {}
        temp_dict['tobs'] = x.tobs
        temp_list.append(temp_dict)

    #session,close()

    return jsonify(temp_list)




if __name__ == '__main__':
    app.run(debug=True, port = 5009)