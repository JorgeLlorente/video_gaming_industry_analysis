import pandas as pd
import numpy as np
import os
import requests
import re
import sqlalchemy as alch
from getpass import getpass


# ------------------------------------------- YOUTUBE --------------------------------------------------

def request_youtube(id_video):

    # This function makes the request to the Youtube API. We choose the parameters we need for our study,
    # and we also provide the IDs ("id_video") we have already extracted.


    token = os.getenv("token")
    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {"part":["snippet", "contentDetails", "statistics"],
           "id": id_video,
           "key":token}

    res = requests.get(url,params=params)
    if res.status_code == 200:
       pass
    else:
      print(res.status_code)
      print(f"Something went wrong with the ID {id_video}")

    return res.json()



def youtube(list_game, game, file):

    # This function calls the request_youtube function, and returns all the data we need
    # for our study.

    results = []
    for id in list_game:
        results.append(request_youtube(id))

    dict_game = {"id": [],
    "title": [],
    "publishedAt": [],
    "channelTitle": [],
    "tags": [],
    "duration": [],
    "viewCount": [],
    "likeCount": [],
    "commentCount": [],
    }

    for result in results:
        if "items" not in list(result.keys()):
            pass
        elif len(result["items"]) == 0:
            pass
        else:
            dict_game["id"].append(result["items"][0]["id"])
            dict_game["title"].append(result["items"][0]["snippet"].get("title"))
            dict_game["publishedAt"].append(result["items"][0]["snippet"].get("publishedAt"))
            dict_game["channelTitle"].append(result["items"][0]["snippet"].get("channelTitle"))
            dict_game["tags"].append(result["items"][0]["snippet"].get("tags"))
            dict_game["duration"].append(result["items"][0]["contentDetails"].get("duration"))
            dict_game["viewCount"].append(result["items"][0]["statistics"].get("viewCount"))
            dict_game["likeCount"].append(result["items"][0]["statistics"].get("likeCount"))
            dict_game["commentCount"].append(result["items"][0]["statistics"].get("commentCount"))

    df_juego = pd.DataFrame(dict_game)
    df_juego["game"] = game
    return df_juego.to_csv(f"../data/youtube/api/{file}_raw")



def concatcsv():
    df1 = pd.read_csv("../data/youtube/api/lol_1_raw")
    df2 = pd.read_csv("../data/youtube/api/lol_2_raw")
    df = pd.concat([df1, df2], axis = 0)



def cleaning(csv, juego_path):

    # In this function we'll clean all the data we have obtained from the API.
    # "Duration" column will be in seconds
    # Numeric columns with NaN will be replaced by the mean of that column.

    df = pd.read_csv(csv)
    df.drop(["Unnamed: 0"], axis=1, inplace=True)
    df["publishedAt"] = df["publishedAt"].str.split("T")
    df.drop(["id", "tags", "title"], axis=1, inplace=True)
    df["publishedAt"] = df["publishedAt"].str[0]
    df["duration"] = df["duration"].str.strip("PT")

    def match(x):
        x = re.findall("\d+\w",x)
        return x

    df["duration"] = df["duration"].apply(match)

    def segundos(x):
        if len(x) == 3:
            tiempo = int(x[0].strip("H")) * 3600 + int(x[1].strip("M")) * 60 + int(x[2].strip("S"))
            return tiempo
        if len(x) == 2:
            if "H" in x[0] and "S" in x[1]:
                tiempo = int(x[0].strip("H")) * 3600 + int(x[1].strip("S"))
                return tiempo
            elif "M" in x[0] and "S" in x[1]:
                tiempo = int(x[0].strip("M")) * 60 + int(x[1].strip("S"))
                return tiempo
            elif "H" in x[0] and "M" in x[1]:
                tiempo = int(x[0].strip("H")) * 3600 + int(x[1].strip("M")) * 60
                return tiempo
        if len(x) == 1:
            if "H" in x[0]:
                tiempo = int(x[0].strip("H")) * 3600
                return tiempo
            elif "M" in x[0]:
                tiempo = int(x[0].strip("M")) * 60
                return tiempo
            elif "S" in x[0]:
                tiempo = int(x[0].strip("S"))
                return tiempo

    df["duration"] = df["duration"].apply(segundos)

    nuevas_columnas = {i: i.lower() for i in df.columns}
    df.rename(columns= nuevas_columnas, inplace = True)

    df["publishedat"] = pd.to_datetime(df["publishedat"])
    df["duration"].replace(np.nan, df["duration"].mean(), inplace = True)
    df["likecount"].replace(np.nan, df["likecount"].mean(), inplace = True)
    df["commentcount"].replace(np.nan, df["commentcount"].mean(), inplace = True)

    return df.to_csv(f"../data/youtube/api/{juego_path}.csv")




    # --------------------------------------- One game analysis ------------------------------------------

def select_sql_table(table):
    db_name = "videogames_industry"
    password = getpass("Contraseña de MySQL: ")
    conexion = f"mysql+pymysql://root:{password}@localhost/{db_name}"
    engine = alch.create_engine(conexion)
    query = f'''SELECT * FROM videogames_industry.{table};'''
    df = pd.read_sql(query, engine)
    return df