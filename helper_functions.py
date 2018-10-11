import json
import requests
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt


def haversine_array(lat1, lng1, lat2, lng2):
    lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
    AVG_EARTH_RADIUS = 6371  # in km
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = np.sin(lat * 0.5) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * np.arcsin(np.sqrt(d))
    return h

def dummy_manhattan_distance(lat1, lng1, lat2, lng2):
    a = haversine_array(lat1, lng1, lat1, lng2)
    b = haversine_array(lat1, lng1, lat2, lng1)
    return a + b

def bearing_array(lat1, lng1, lat2, lng2):
    AVG_EARTH_RADIUS = 6371  # in km
    lng_delta_rad = np.radians(lng2 - lng1)
    lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
    y = np.sin(lng_delta_rad) * np.cos(lat2)
    x = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(lng_delta_rad)
    return np.degrees(np.arctan2(y, x))

def speed(w, h):
    """Return speed_table"""
    df = pd.read_csv('db/avg_speed.csv')
    avg_speed = df[(df['Weekday']==w) & (df['Hour']==h)]['speed_m']
    return avg_speed

def get_coordinate(pick, drop):
    pick_url = "https://nominatim.openstreetmap.org/search/" + pick + "?format=json"
    drop_url = "https://nominatim.openstreetmap.org/search/" + drop + "?format=json"
    
    p_response = requests.get(pick_url).json()
    d_response = requests.get(drop_url).json()
    
    
    # pick up lat and lon
    p_lat = p_response[0]['lat']
    p_lng =  p_response[0]['lon']
    
    # drop off lat and lon
    d_lat = d_response[0]['lat']
    d_lng =  d_response[0]['lon']
    
    coordinate = {'p_lat': float(p_lat),
                  'p_lng': float(p_lng),
                 'd_lat': float(d_lat),
                  'd_lng': float(d_lng),
                 }
    
    return coordinate