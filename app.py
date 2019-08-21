import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes.passenger

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all prcp names"""
    # Query all prcp
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Meausurement.date >= '2016-10-01').\
        group_by(Measurement.date).all()

    all_precipitation = []

    # Query for the dates and temperature observations from the last year.
    for result in results:
        precipitation_dict = {}
        precipitation_dict["date"] = result[0]
        precipitation_dict["prcp"] = result[1]
        all_precipitation.append(precipitation_dict)

        return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all the stations"""
    # Query all stations
    results = session.query(Measurement.station).group_by(
        Measurement.station).all()
    all_sessions = list(np.ravel(results))
    
    return jsonify(all_sessions)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperature observations (tobs) for the previous year"""
    # Query all tobs for the previous year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-10-01').all()

    all_tobs = []

    for result in results:
        tobs_dict = {}
        tobs_dict["date"] = result[0]
        tobs_dict["tobs"] = result[1]
        all_tobs.append(tobs_dict)
        return jsonify(all_tobs)


if __name__ == '__main__':
    app.run(debug=True)
