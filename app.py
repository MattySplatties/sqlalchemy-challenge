#For some reason, this code works in spyder but gave errors in VS Code, any idea why...???
#Matt Channell- Module 10

# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base


from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """All available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
#running query
def rainlastyear():
    #Query for last 12 months
    year_ago = dt.date(2016,8,23)
    sel = [Measurement.date, func.max(Measurement.prcp)]
    lastyear = session.query(*sel).filter(Measurement.date > year_ago).group_by(Measurement.date).all()

    session.close()

    #Creating Dictionary
    rain_prcp = {"Date":[], "Prcp":[]}
    for date, prcp in lastyear:
        rain_prcp["Date"].append(date)
        rain_prcp["Prcp"].append(prcp)

    return jsonify(rain_prcp)


@app.route("/api/v1.0/stations")
def station():
    #Query for stations
    results = session.query(Station.station).all()
    session.close()
    
    #Converts to normal list, to then jsonify
    Stations = list(np.ravel(results))
    return jsonify(Stations)

@app.route('/api/v1.0/tobs')
def temp():
    #Query of temps
    sel2 = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    temp = session.query(*sel2).filter(Measurement.station == 'USC00519281').all()
    session.close()
    
    #Converts to normal list, to then jsonify
    Temperature = list(np.ravel(temp))
    return jsonify(Temperature)

@app.route('/api/v1.0/<start>')
def starts(start):
    #Query including start date from the URL as variable
    sel3 = [Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    startdate = session.query(*sel3).filter(Measurement.date >= start).group_by(Measurement.date).all()
    
    session.close()
    
    #Dictionary of info
    start_dict = {"Date":[], "Min Temp":[], "Max Temp":[], "Avg Temp":[]}
    for date, min, max, avg in startdate:
        start_dict["Date"].append(date)
        start_dict["Min Temp"].append(min)
        start_dict["Max Temp"].append(max)
        start_dict["Avg Temp"].append(avg)
        
    return jsonify(start_dict)

@app.route('/api/v1.0/<start>/<end>')
def startend(start,end):
    #Query including start and end date from the URL as variables
    sel4 = [Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    startenddate = session.query(*sel4).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    session.close()
    
    #Dictionary of info
    startend_dict = {"Date":[], "Min Temp":[], "Max Temp":[], "Avg Temp":[]}
    for date, min, max, avg in startenddate:
        startend_dict["Date"].append(date)
        startend_dict["Min Temp"].append(min)
        startend_dict["Max Temp"].append(max)
        startend_dict["Avg Temp"].append(avg)
        
    return jsonify(startend_dict)
        


if __name__ == '__main__':
    app.run()
