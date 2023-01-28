import streamlit as st
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

with open('data/top10_games.pickle', 'rb') as game:
    games = pickle.load(game)
list_games = games[1:]

juego = st.selectbox('Pick one', list_games)

st.write(sp.info(juego))