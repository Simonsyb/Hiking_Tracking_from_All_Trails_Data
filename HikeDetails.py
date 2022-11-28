from math import radians, cos, sin, asin, sqrt
import datetime
import numpy as np
import pandas as pd

def get_Date(df):
    time_column_idx = df.columns.get_loc("time")
    return str(df.iat[0, time_column_idx])[0:-9]


def longLat_dist(lat1, lat2, long1, long2):
    long1 = radians(long1)
    long2 = radians(long2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlong = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlong / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return (c*r)

def total_dist(df):
    lat_column_idx = df.columns.get_loc("latitude")
    long_column_idx = df.columns.get_loc("longitude")
    dist = 0

    for i in range(df.shape[0]):
        if i == 0:
            pass
        else:
            dist += longLat_dist(df.iat[i-1, lat_column_idx], df.iat[i, lat_column_idx], df.iat[i-1, long_column_idx],df.iat[i, long_column_idx])
    return dist



def hike_duration(df):
    start_time=str(df.iat[0, 0])[:-6]
    end_time=str(df.iat[df.shape[0] - 1, 0])[:-6]

    format = '%Y-%m-%d %H:%M:%S'
    startDateTime = datetime.datetime.strptime(start_time, format)
    endDateTime = datetime.datetime.strptime(end_time, format)

    total_time = endDateTime - startDateTime
    return(total_time)


def avg_pace(df):
    time_formated = hike_duration(df)
    total_distance = total_dist(df)
    final_pace = time_formated/total_distance
    final_pace = str(final_pace).split(".")[0]
    return(final_pace)


def total_elvGain(df):
    elv_column_idx = df.columns.get_loc("elevation")
    elv_gain = 0

    for i in range(df.shape[0]):
        if i == 0 or df.iat[i-1, elv_column_idx] == df.iat[i, elv_column_idx] or  df.iat[i-1, elv_column_idx] > df.iat[i, elv_column_idx]:
            pass
        elif df.iat[i-1, elv_column_idx] < df.iat[i, elv_column_idx]:
            elv_gain+= (df.iat[i, elv_column_idx]-df.iat[i-1, elv_column_idx])
    return round(elv_gain,2)

def total_elvLoss(df):
    elv_column_idx = df.columns.get_loc("elevation")
    elv_loss = 0

    for i in range(df.shape[0]):
        if i == 0 or df.iat[i-1, elv_column_idx] == df.iat[i, elv_column_idx] or  df.iat[i-1, elv_column_idx] < df.iat[i, elv_column_idx]:
            pass
        elif df.iat[i-1, elv_column_idx] > df.iat[i, elv_column_idx]:
            elv_loss+= (df.iat[i-1, elv_column_idx]-df.iat[i, elv_column_idx])
    return round(elv_loss,2)