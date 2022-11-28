import gpxpy
import os
import pandas as pd
import HikeDetails

def create_df(path_name):
    gpx_path = path_name
    with open(gpx_path) as f:
        gpx = gpxpy.parse(f)

    points = []
    for segment in gpx.tracks[0].segments:
        for p in segment.points:
            points.append({
                'time': p.time,
                'latitude': p.latitude,
                'longitude': p.longitude,
                'elevation': p.elevation,
            })
    df = pd.DataFrame.from_records(points)
    return df
