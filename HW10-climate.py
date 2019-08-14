from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///data/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine) 

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = session.query(Measurement.date, Measurement.prcp).all()
    prcp_data = []

    for date,prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def station():
    
    results = session.query(Station.name).all()
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = dt.date(2016, 8, 23)
    results = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.date > year_ago).\
              order_by(Measurement.date).all()       
    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii cimate data!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2017-01-01<br/>"
        f"/api/v1.0/2015-01-01/2017-08-01"
    )


@app.route("/api/v1.0/<start>")
def start(start):
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temp_1 = session.query(*sel).filter(Measurement.date >= start).all()
    return jsonify(temp_1)

@app.route("/api/v1.0/<datestart>/<dateend>")
def start_end(datestart,dateend):
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temp_2 = session.query(*sel).filter(Measurement.date >= datestart).filter(Measurement.date <= dateend).all()
    return jsonify(temp_2)

if __name__ == "__main__":
    app.run(debug=True)