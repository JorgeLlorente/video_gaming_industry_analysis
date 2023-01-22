import pandas as pd
import numpy as np
import os
import requests
import re
import sqlalchemy as alch
from getpass import getpass
from dotenv import load_dotenv
import pickle
import matplotlib.pyplot as plt
import sys
sys.path.append("../")

import src.support as sp


# ------------------------------------------- General Overview -------------------------------------------

def genre_through_time():
    genre = input("Introduce a genre: ")
    df_genre = df_genres2[df_genres2["genre"] == genre].groupby([df_genres2['release_date'].dt.year])["videogame_id"].count().reset_index()

    fig = plt.bar(df_genre["release_date"], df_genre["videogame_id"], color="blue", edgecolor="black", label="count")
    plt.ylabel("Score")
    plt.axhline(y=df_genre["videogame_id"].mean(), color="red")
    plt.legend()
    plt.xticks(rotation=45);


    # --------------------------------------- One game analysis ------------------------------------------

def sql_connection():
    db_name = "videogames_industry"
    sql = os.getenv("MySQLPassword")
    conexion = f"mysql+pymysql://root:{sql}@localhost/{db_name}"
    engine = alch.create_engine(conexion)


def select_sql_table(table):

    # This function does the next three things
    # 1. Function makes the connection with MySQL.
    # 2. Function corrects columns type.
    # 3. Function filter table by top 10 videogames.


    db_name = "videogames_industry"
    sql = os.getenv("MySQLPassword")
    conexion = f"mysql+pymysql://root:{sql}@localhost/{db_name}"
    engine = alch.create_engine(conexion)

    query = f'''SELECT * FROM videogames_industry.{table};'''
    df = pd.read_sql(query, engine)
    if "fecha" in df.columns and "watch_time_hours" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"])
        df["watch_time_hours"] = df["watch_time_hours"].astype("float")
    elif "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"])

    else:
        pass
    with open('../data/top10_games.pickle', 'rb') as game:
        games = pickle.load(game)
    df = df[df["videogame_id"].isin(games)]
    return df


def plotting(df_game, df_all, juego):

    # In this function we will visualize timeline plots depending on the game we are choosing and
    # the dataframes we have chosen. Dataframes depend on the columns we want to analyze.

    plt.rcParams["figure.figsize"] = [8.0, 2.0]

    for i, column in zip(range(len(list(df_game.columns))), list(df_game.columns)):
        if column == "fecha":
            pass
        else:
            fig = plt.figure(f"Figure {i}")
            plt.title(f"mean of {column} in {juego}")
            plt.xlabel("Year")
            plt.ylabel(column)
            # plt.legend()
            plt.plot(df_all["fecha"],
                    df_all[column],
                    color = "grey",
                    linewidth = 2,
                    marker = "o")
                    # label= "mean")

            plt.plot(df_game["fecha"],
                    df_game[column],
                    color = "black",
                    linewidth = 2,
                    marker = "o")
                    # label= "Fortnite")
            plt.show()

def info(juego):

    # This function return main features of a specific game.

    print(f"General features from {juego}: ")
    df_genres = sp.select_sql_table("genres")
    df_genres = df_genres[df_genres["videogame_id"] == juego]
    print(f'Belongs to genres {", ".join(df_genres["genre"].to_list())}')

    df_platforms = sp.select_sql_table("platforms")
    df_platforms = df_platforms[df_platforms["videogame_id"] == juego]
    print(f'It is available on the next platforms: {", ".join(df_platforms["platform"].to_list())}')


    df_info_general = sp.select_sql_table("info_general")
    df_info_general = df_info_general[df_info_general["videogame_id"] == juego]
    print(f'The game developer is {", ".join(df_info_general["developer"].to_list())}')
    print(f'Players type game: {", ".join(df_info_general["jugadores"].to_list())}')

    df_games_unique = sp.select_sql_table("videogames_unique")
    df_games_unique = df_games_unique[df_games_unique["videogame_id"] == juego]
    print(f'Metacritics score is {list(df_games_unique["meta_score"])[0]}')
    print(f'User review score is {list(df_games_unique["user_review"])[0]}')

def data_visualization():

    # This function returns time graphics for a game and a table chosen from MySQL

    with open('../data/top10_games.pickle', 'rb') as game:
        games = pickle.load(game)
    list_games = games
    
    list_of_tables = ["torneos", "youtube", "twitch"]

    # Defining the input table
    juego = input(f"Choose a game from the list ({list_games}): ")
    table = input(f"Choose a table from MySQL({list_of_tables}): ")
    df = sp.select_sql_table(table)

    # General features of the game

    sp.info(juego)

    # Creating df for comparisons
    columns = df.columns
    data = str.split(input(f"Choose the data you want to visualize ({df.columns}): "), ", ")
    df_all = df.groupby(by=df["fecha"].dt.year)[data].mean().reset_index()
    df_game = df[df["videogame_id"] == juego]
    df_game = df_game.groupby(by=df_game["fecha"].dt.year)[data].mean().reset_index()

    # Plotting
    sp.plotting(df_game,df_all,juego)