import os
import gpxToDf
import HikeDetails
import datetime
import pandas as pd

def get_pace(df):
    lat_column_idx = df.columns.get_loc("latitude")
    long_column_idx = df.columns.get_loc("longitude")
    format = '%H:%M:%S'

    elv_collection = []
    pace_collection = []
    km_collection = [1]
    dist = 0
    counter = 1
    total_dist = HikeDetails.total_dist(df)

    start_time = str(df.iat[0, 0])[11:-6]

    for i in range(df.shape[0]):
        if i == 0:
            pass
        else:
            dist += HikeDetails.longLat_dist(df.iat[i - 1, lat_column_idx], df.iat[i, lat_column_idx],df.iat[i - 1, long_column_idx],df.iat[i, long_column_idx])
        if dist == total_dist:
            end_time = str(df.iat[i - 1, 0])[11:-6]
            startDateTime = datetime.datetime.strptime(start_time, format)
            endDateTime = datetime.datetime.strptime(end_time, format)
            pace_collection.append(str(endDateTime - startDateTime)[2:])
        elif dist >= counter:
             end_time = str(df.iat[i-1, 0])[11:-6]
             startDateTime = datetime.datetime.strptime(start_time, format)
             endDateTime = datetime.datetime.strptime(end_time, format)
             pace_collection.append(str(endDateTime - startDateTime)[2:])
             start_time=str(df.iat[i-1, 0])[11:-6]
             if counter+1 > HikeDetails.total_dist(df):
                 counter = total_dist
             else:
                 counter+=1
             km_collection.append(round(counter,2))

    new_df = pd.DataFrame(list(zip(km_collection, pace_collection)),
                      columns=['KM', 'Pace'])
    return new_df

