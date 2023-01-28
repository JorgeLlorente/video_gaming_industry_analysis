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
import datetime
import sys
sys.path.append("../")

import src.support as sp


# ------------------------------------------- General Overview -------------------------------------------

def genre_over_time():
    genre = input("Choose a genre: ")
    df_genre = df_genres2[df_genres2["genre"] == genre].groupby([df_genres2['release_date'].dt.year])["videogame_id"].count().reset_index()

    fig = plt.bar(df_genre["release_date"], df_genre["videogame_id"], color="blue", edgecolor="black", label="count")
    plt.ylabel("Score")
    plt.axhline(y=df_genre["videogame_id"].mean(), color="red")
    plt.legend()
    plt.xticks(rotation=45);


    # --------------------------------------- One game analysis ------------------------------------------

def select_sql_table(table):

    # This function does the next three things
    # 1. It creates the connection with MySQL.
    # 2. It corrects columns type.
    # 3. It filters table by top 10 videogames.


    # Args
    # - Table: name of one of the tables contained in the database.


    db_name = "videogames_industry"
    sql = os.getenv("MySQLPassword")
    conexion = f"mysql+pymysql://root:{sql}@localhost/{db_name}"
    engine = alch.create_engine(conexion)

    query = f'''SELECT * FROM videogames_industry.{table};'''
    df = pd.read_sql(query, engine)

    # Here we will include all columns that aren't imported in the right type

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


def plotting_years(df_game, df_all, juego):

    # In this function we will visualize timeline plots depending on the game we are choosing and
    # the dataframes we have chosen. Dataframes depend on the columns we want to analyze.

    # Args:
    # - df_game: table filtered by game.
    # - df_all: table containing all games.
    # - juego: game we want to filter in df_game.

    plt.rcParams["figure.figsize"] = [8.0, 2.0]

    for i, column in zip(range(len(list(df_game.columns))), list(df_game.columns)):
        if column == "fecha":
            pass
        else:
            fig = plt.figure(f"Figure {i}")
            plt.title(f"mean of {column} in {juego}")
            plt.xlabel("Year")
            plt.ylabel(column)

            plt.plot(df_all["fecha"],
                    df_all[column],
                    color = "grey",
                    linewidth = 2,
                    marker = "o",
                    label= "mean of games")

            plt.plot(df_game["fecha"],
                    df_game[column],
                    color = "blue",
                    linewidth = 2,
                    marker = "o",
                    label= "Fortnite")
            plt.legend()
            plt.show()

def plotting_months(df_game, df_all, juego, year):

        # In this function we will visualize timeline plots depending on the game we are choosing and
        # the dataframes we have chosen. Dataframes depend on the columns we want to analyze.

            plt.rcParams["figure.figsize"] = [8.0, 2.0]

            for i, column in zip(range(len(list(df_game.columns))), list(df_game.columns)):
                if column == "fecha":
                    pass
                else:
                    fig = plt.figure(f"Figure {i}")
                    plt.title(f"mean of {column} in {juego} during year {year}")
                    plt.xlabel("Months")
                    plt.ylabel(column)
                    meses = [datetime.date(year, m, 1).strftime('%B') for m in range(13 - df_game.shape[0], 13)]

                    plt.xticks(df_game["fecha"], meses, rotation=45)

                    plt.plot(df_all["fecha"],
                            df_all[column],
                            color = "grey",
                            linewidth = 2,
                            marker = "o",
                            label= "mean of games")

                    plt.plot(df_game["fecha"],
                            df_game[column],
                            color = "blue",
                            linewidth = 2,
                            marker = "o",
                            label= juego)
                    plt.legend()
                    plt.show()


def info(juego):

    # This function return main features of a specific game.

    print(f"General features of {juego}: ")
    df_genres = sp.select_sql_table("genres")
    df_genres = df_genres[df_genres["videogame_id"] == juego]
    print(f'- Belongs to genres {", ".join(df_genres["genre"].to_list())}')

    df_platforms = sp.select_sql_table("platforms")
    df_platforms = df_platforms[df_platforms["videogame_id"] == juego]
    print(f'- It is available on the next platforms: {", ".join(df_platforms["platform"].to_list())}')


    df_info_general = sp.select_sql_table("info_general")
    df_info_general = df_info_general[df_info_general["videogame_id"] == juego]
    print(f'- The game developer is {", ".join(df_info_general["developer"].to_list())}')
    print(f'- Players type game: {", ".join(df_info_general["jugadores"].to_list())}')

    df_games_unique = sp.select_sql_table("videogames_unique")
    df_games_unique = df_games_unique[df_games_unique["videogame_id"] == juego]
    print(f'- Metacritics score is {list(df_games_unique["meta_score"])} out of 100')
    print(f'- User review score is {list(df_games_unique["user_review"])} out of 10')

def data_visualization():

    # This function returns time graphics for a game and a table chosen from MySQL

    with open('../data/top10_games.pickle', 'rb') as game:
        games = pickle.load(game)
    list_games = games[1:]

    list_of_tables = ["torneos", "youtube", "twitch"]

    # General features of the game
    juego = input(f"Choose a game from the list ({list_games}): ")
    sp.info(juego)

    # Defining the input table
    table = input(f"Choose a table from MySQL({list_of_tables}): ")
    df = sp.select_sql_table(table)

    # Creating df for comparisons
    type = input("Do you want a global analysis or a year analysis? Choose between global or year: ")

    if type == "global":

        columns = df.columns
        data = str.split(input(f"Choose the data you want to visualize ({df.columns}): "), ", ")
        df_all = df.groupby(by=df["fecha"].dt.year)[data].mean().reset_index()
        df_game = df[df["videogame_id"] == juego]
        df_game = df_game.groupby(by=df_game["fecha"].dt.year)[data].mean().reset_index()

        # Plotting global
        sp.plotting_years(df_game, df_all, juego)

    elif type == "year":
        year = int(input("Choose a year: "))
        columns = df.columns
        data = str.split(input(f"Choose the data you want to visualize ({df.columns}): "), ", ")
        df_all = df.groupby(by=[df.fecha.dt.year, df.fecha.dt.month])[data].mean()
        df_all = df_all.loc[year].reset_index()
        df_game = df[df["videogame_id"] == juego]
        df_game = df_game.groupby(by=[df.fecha.dt.year, df.fecha.dt.month])[data].mean()
        df_game = df_game.loc[year].reset_index()

        # Plotting one year
        sp.plotting_months(df_game, df_all, juego, year)



# -------------------------------------------- Analysis tool ----------------------------------------------

def selecting_tables():

# Connection

    db_name = "videogames_industry"
    sql = os.getenv("MySQLPassword")
    conexion = f"mysql+pymysql://root:{sql}@localhost/{db_name}"
    engine = alch.create_engine(conexion)

# Selecting tables

    query_all = '''SELECT table_name
                FROM information_schema.tables
                WHERE table_type='BASE TABLE'
                AND table_schema = 'videogames_industry';'''

    df = pd.read_sql(query_all, engine)
    list_tables = df["TABLE_NAME"].to_list()
    main_table = input(f"Type the main table (one of the list -> {list_tables}): ")
    list_tables.remove(main_table)

    texto = ""
    a = "Yes"
    while a == "Yes":
        a = input("Do you want to add another table? Yes/No: ")
        if a == "No":
            break
        else:
            table = input(f"Type a new table from the list (one of the list -> {list_tables}): ")
            query_secondary_table = f'''INNER JOIN {table}
                                        ON {main_table}.videogame_id = {table}.videogame_id '''
            texto = texto + query_secondary_table
            list_tables.remove(table)
    query = f'''SELECT *
    FROM videogames_industry.{main_table}
    {texto};'''

    df = pd.read_sql(query, engine)
    df = df.loc[:,~df.columns.duplicated()]

# Selecting columns and giving them the right type (due to errors when bringing data from MySQL)

    columnas = input(f"Type the columns you want to analyze(from the list{df.columns}")
    columnas = columnas.split(", ")
    columnas
    df = df[columnas]

# Here we will include all columns that aren't imported in the right type

    if "fecha" in df.columns and "watch_time_hours" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"])
        df["watch_time_hours"] = df["watch_time_hours"].astype("float")
    elif "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"])
    else:
        pass

# Now we filter by top 10 video games --> Next job: giving each game a certain level of impact.
    with open('../data/top10_games.pickle', 'rb') as game:
        games = pickle.load(game)
    df = df[df["videogame_id"].isin(games)]

    return df


def info(juego):

    # This function return main features of a specific game.

    print(f"General features of {juego}: ")
    df_genres = sp.select_sql_table("genres")
    df_genres = df_genres[df_genres["videogame_id"] == juego]
    print(f'- Belongs to genres {", ".join(df_genres["genre"].to_list())}')

    df_platforms = sp.select_sql_table("platforms")
    df_platforms = df_platforms[df_platforms["videogame_id"] == juego]
    print(f'- It is available on the next platforms: {", ".join(df_platforms["platform"].to_list())}')


    df_info_general = sp.select_sql_table("info_general")
    df_info_general = df_info_general[df_info_general["videogame_id"] == juego]
    print(f'- The game developer is {", ".join(df_info_general["developer"].to_list())}')
    print(f'- Players type game: {", ".join(df_info_general["jugadores"].to_list())}')

    df_games_unique = sp.select_sql_table("videogames_unique")
    df_games_unique = df_games_unique[df_games_unique["videogame_id"] == juego]
    print(f'- Metacritics score is {list(df_games_unique["meta_score"])} out of 100')
    print(f'- User review score is {list(df_games_unique["user_review"])} out of 10')


def data_visualization_tool():
    with open('../data/top10_games.pickle', 'rb') as game:
        list_games = pickle.load(game)

    # General features of the game
    juego = input(f"Choose a game from the list ({list_games}): ")

    sp.info(juego)

    # Defining the input table

    df = sp.selecting_tables()

    # Creating df for comparisons

    type = input("Do you want a global analysis or a year analysis? Choose between global or year: ")

    if type == "global":

        columns = df.columns
        data = str.split(input(f"Choose the data you want to visualize ({columns}): "), ", ")
        df_all = df.groupby(by=df["fecha"].dt.year)[data].mean().reset_index()
        df_game = df[df["videogame_id"] == juego]
        df_game = df_game.groupby(by=df_game["fecha"].dt.year)[data].mean().reset_index()

        # Plotting global
        sp.plotting_years(df_game, df_all, juego)

    elif type == "year":
        year = int(input("Choose a year: "))
        columns = df.columns
        data = str.split(input(f"Choose the data you want to visualize ({df.columns}): "), ", ")
        df_all = df.groupby(by=[df.fecha.dt.year, df.fecha.dt.month])[data].mean()
        df_all = df_all.loc[year].reset_index()
        df_game = df[df["videogame_id"] == juego]
        df_game = df_game.groupby(by=[df.fecha.dt.year, df.fecha.dt.month])[data].mean()
        df_game = df_game.loc[year].reset_index()

        # Plotting one year
        sp.plotting_months(df_game, df_all, juego, year)
