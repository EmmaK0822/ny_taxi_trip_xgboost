################
# DEPENDENCIES #
################
import os.path
import json
import sqlite3
from helper_functions import speed, haversine_array, dummy_manhattan_distance, bearing_array, get_coordinate
from datetime import datetime, date, time
from init_db import speed_table

import pandas as pd
import numpy as np

import xgboost
import pickle

from flask import Flask, jsonify, render_template, request, redirect

#############
# FLASK APP #
#############
app = Flask(__name__)

###############
# MAIN ROUTES #
###############
@app.route("/")
def index():
    """Return index page"""
    return render_template('index.html')

@app.route("/send", methods=["GET", "POST"])
def xgb():
    if request.method == "POST":
        """ Getting coordinates """
        p_address = request.form["pickup"]
        d_address = request.form["dropoff"]

        coordinate = get_coordinate(p_address, d_address)

        pickup_lat = coordinate['p_lat']
        pickup_lng = coordinate['p_lng']
        dropoff_lat = coordinate['d_lat']
        dropoff_lng = coordinate['d_lng']

        print(pickup_address)
        print(dropoff_address)
        
        """ Getting date/time values """
        schedule = request.form["schedule"]

        if schedule == "now":
            today = datetime.now()
            date = today.weekday() # Return the day of the week as an integer, where Monday is 0 and Sunday is 6
            hour = today.hour()
        else:
            date = request.form["weekday"] # convert string to datetime
            time = request.form["time"]
            hour = time.hour()
        
        print(today)
        print(date)
        print(time)

        """ Data Preprocessing """
        distance = dummy_manhattan_distance(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng)
        speed = speed(date, hour)
        direction = bearing_array(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng)
        """ Load the unique possibility training dataset """

        train = # either load the unique dataset from csv or create a fake dataset

        """ Creating dataframe to feed a model """
        test = pd.DataFrame({
            'date': date,
            'time': time,
            'distance_m': distance,
            'direction': direction,
            'avg_speed_m': speed
        })

        """ Concat """"
        pd.concat([train, test])

        """ Dummfied """
        pd.get_dummies

        """ Extract the test data """
        test = df.iloc[-1]

        """ Load the model """
        model = pickle.load(open("ny_taxi.pickle.dat", "rb"))

        """ Run the model """
        prediction = model.predict(test)

        """ Option 2. Save the prediction to DB """
        # save the prediction and generate an unique ID
        # store the prediction and unique ID (maybe time) in DB
        # 

        return redirect(f"/result/{prediction}/{time}", code=302)

    return render_template("learn.html")    


@app.route("/result/<prediction>/<time>")
def visualization(prediction, time):
    """ Option 1. Using Jinja """"
    results = {"pred": prediction}

    """ Option 2. Query the prediction """ 
    ### how can I prevent multiple queries

    """Return the prediction"""
    return render_template('result.html', results=results)

################################
# INITIALIZE SPEED DATABASE #
################################
@app.before_first_request
def init_db():
    # check if db exists
    db_exists = os.path.exists(db_path)
    db_status = False

    # if db and all tables exist, pass
    if db_exists:
        db_status = exists_table("speed", db_path) and exists_table(
            "speedByTime", db_path)
        if db_status:
            pass
        # if not all tables exist, remove db
        else:
            os.remove(db_path)

    # if all tables exist, pass
    if db_status:
        pass
    # else build db and all tables
    else:
        build_speed_table()

if __name__ == "__main__":
    app.run(debug=True, port=4996)
