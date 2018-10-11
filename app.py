################
# DEPENDENCIES #
################
import os.path
import json
import sqlite3
from math import radians, cos, sin, asin, sqrt
from helper_functions import speed, haversine_array, dummy_manhattan_distance, bearing_array, get_coordinate
import datetime
from datetime import date

import pandas as pd
import numpy as np

import xgboost
import pickle

from flask import Flask, jsonify, render_template, request, redirect

#############
# FLASK APP #
#############
application = Flask(__name__)

###############
# MAIN ROUTES #
###############
@application.route("/")
def index():
    """Return index page"""
    return render_template('index.html')

@application.route("/send", methods=["GET", "POST"])
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

        print(p_address)
        print(d_address)
        print(coordinate)
        
        """ Getting date/time values """
        schedule = request.form["schedule"]

        if schedule == "now":
            day = date.today()
            week = day.weekday() # Return the day of the week as an integer, where Monday is 0 and Sunday is 6
            now = datetime.datetime.now()
            hr = now.hour
        else:
            week = request.form["weekday"] # convert string to datetime -> no need
            time = request.form["time"] # confirm the value -> 02:03 PM (14%3A03)
            hr = time[:1]

        print(week)
        print(hr)

        """ Data Preprocessing """
        distance = dummy_manhattan_distance(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng)
        avg_speed = speed(week, hr)
        direction = bearing_array(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng)
        
        """ Load the unique possibility training dataset """
        # either load the unique dataset from csv or create a fake dataset
        train = pd.read_csv('db/avg_speed.csv')

        """ Creating dataframe to feed a model """
        test = pd.DataFrame({
            'Weekday': week,
            'Hour': hr,
            'distance_dummy_manhattan': distance,
            'direction': direction,
            'avg_speed_m': avg_speed
        }, index=[168])

        """ Concat """
        df = pd.concat([train, test])

        """ Dummfied """
        df = pd.get_dummies(df, columns=['Weekday', 'Hour'])

        """ Extract the test data """
        test = df.iloc[[-1]]

        """ """
        test = test[['distance_dummy_manhattan', 'direction', 'avg_speed_m', 'Hour_0', 'Hour_1', 'Hour_2', 'Hour_3', 'Hour_4', 'Hour_5', 'Hour_6', 'Hour_7', 'Hour_8', 'Hour_9', 'Hour_10', 'Hour_11', 'Hour_12', 'Hour_13', 'Hour_14', 'Hour_15', 'Hour_16', 'Hour_17', 'Hour_18', 'Hour_19', 'Hour_20', 'Hour_21', 'Hour_22', 'Hour_23', 'Weekday_0', 'Weekday_1', 'Weekday_2', 'Weekday_3', 'Weekday_4', 'Weekday_5', 'Weekday_6']]
        test_dmatrix = xgboost.DMatrix(test)

        """ Load the model """
        model = pickle.load(open("db/new_model.pickle.dat", "rb"))

        """ Run the model """
        prediction = model.predict(test_dmatrix)

        pred = prediction[0]

        """ Option 2. Save the prediction to DB """
        # save the prediction and generate an unique ID
        # store the prediction and unique ID (maybe time) in DB

        """ Redirect the route with values """
        # example: redirect(f"/result/{prediction}/{time}/{speed}", code=302)
        # app route should have same format: @app.route("/result/<prediction>/<time>/<speed>")
        # use the value as input: def whateverfuction(prediction, time, speed)

        return redirect(f"/result/{pred}", code=302)

    return render_template("/")    


@application.route("/result/<pred>")
def visualization(pred):
    """ Option 1. Using Jinja """
    results = {"pred": pred}

    """ Option 2. Query the prediction """ 
    ### how can I prevent multiple queries

    """Return the prediction"""
    return render_template('result.html', results=results)


if __name__ == "__main__":
    application.run(debug=True, port=4996)
