import sqlite3
import HikeDetails
import gpxToDf
import os

import pacePerKM


def create_main_db():
    conn = sqlite3.connect('HikingStats.db')
    c = conn.cursor()

    c.execute("""
    CREATE TABLE HikesSummary (
    
    ID INTEGER PRIMARY KEY,
    Name TEXT,
    Date TEXT,
    Start_Time TEXT,
    Distance_KM INTEGER,
    Duration TEXT,
    Average_Pace TEXT,
    Elevation_Gain_M INTEGER,
    Elevation_Loss_M INTEGER
    )""")

    conn.commit()
    conn.close()

def insert_MainVal():
    conn = sqlite3.connect('HikingStats.db')
    c = conn.cursor()
    root = "/Users/simonsybydlo/Desktop/Alltrials app/Personal Hike Data/"

    for filename in os.listdir(root):
        if not filename.startswith('.') and os.path.isfile(os.path.join(root, filename)):
            df = gpxToDf.create_df(str(root + filename))
            paceDF= pacePerKM.get_pace(df)
            paceDF.to_sql(filename, conn, if_exists='replace', index=False)
            insert_str="INSERT INTO HikesSummary VALUES(NULL,'"+filename[:-4].replace("'", "")+"','"+str(HikeDetails.get_Date(df))[:-6]+"','"+str(HikeDetails.get_Date(df))[-5:]+"',"+str(round(HikeDetails.total_dist(df),2))+",'"+str(HikeDetails.hike_duration(df))+"','"+HikeDetails.avg_pace(df)+"',"+str(HikeDetails.total_elvGain(df))+","+str(HikeDetails.total_elvLoss(df))+")"
            c.execute(insert_str)

    conn.commit()
    conn.close()

def select_Star():
    conn = sqlite3.connect('HikingStats.db')
    c = conn.cursor()
    c.execute("SELECT * FROM HikesSummary")


create_main_db()
insert_MainVal()
select_Star()