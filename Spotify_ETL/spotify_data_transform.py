# This file builds on the base code established in spotify_data_extract.py
# See that file for comment breakdown of each part.

import pandas as pd
import requests
import json
from datetime import datetime
import datetime

DATABASE_LOCATION = "sqlite:///my_played_tacks"
USER_ID = "22spaqn7osucmwakfga7772dq"
TOKEN = "BQDqJo9-H097aPASSqglrb7OVk8WL9-Aoewl8enVj8KLRlVeUKKLQa5WEWvU5rDO_-32h8AKluLafjOvPt6hcH6db_yTTrjfjUiWFhZx6h0D9-n5BPz9c3-pbN48cfuz6Dal0KMm2TVRNzIhhh9YSeVTcQn_sDRG73mjL5e1" # insert Spotify key here
# Create a function that will validate the data that comes in, to make
# sure it's consistent with what we expect.

def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if the dataframe is empty 
    
    # It could be an error, or you just didn't listen to Spotify in the last 24 hrs.
    if df.empty:
        print("No songs played. Finishing execution")
        return False

    # Primary key check
    # Using the played_at col as the PK since in Spotify it must be unique.
    # If there's a duplicate, there must be an error:
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    # We're not going to allow any nulls here
    if df.isnull().values.any():
        raise Exception("Null values found")

    # Validate the timestamp. If not all the timestamps are == yesterday,
    # we want the feed to fail.
    #  Amend the yesterday variable so it doesn't get more granular than a day
    #  because we're comparing it to the timestamp variable which does not contain
    #  hours, minutes & seconds data (simply setting all those fields to 0).
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        # timestamps will be from yesterday, strptime strips everything but the specified Y M D info
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception("At least one of the returned songs does not have a yesterday's timestamp")
    
    return True

if __name__ == "__main__":
    
    headers = {
        "Accept" : "application",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)
    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    
    for song in data["items"]:
        song_names.append(song["track"]["name"]) 
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name" : song_names,
        "artist_name" : artist_names,
        "played_at" : played_at_list,
        "timestamps" : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamps"])
    print(song_df)

    # Validate
    if check_if_valid_data(song_df):
        print("Data valid, proceed to Load stage")

