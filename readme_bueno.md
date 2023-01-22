# Video games Industry Analysis

![](../videogames_industry/images/videogames_title.jfif)

Since first desktop computer video games like Pac-Man, video games industry has been evolving to deliver the best entertainment to users.

The goal of this project is divided into two parts:

- Obtain a general overview from the video games industry.
- Compare games to their peers and draw conclusions about their actual performance.

## Why this project

 The reason why I have chosen this topic is due to my curiosity and interest in the video game industry.

 This is a 2 week project supervised by Ironhack Data Analytics Bootcamp instructors.

## Data acquisition

### Metacritics Video games from Kaggle

This is a CSV containing around 18.000 video games released since 1995 until 2022.

### Using Selenium to obtain genres

I have used Metacritics URL to also extract genres from a subset of games (around 500)

### Web scraping to obtain tourneys

I have used a web page called "esportsearning" to obtain all the tourneys played since 2012.

### Using Selenium to obtain Twitch info about video games performance

In this dataset, I have downloaded a total of 84 .csv files about video games performance in Twitch

### Using Selenium and Youtube API to obtain info about video games performance

In order to adapt to the number of requests available in the free trial account, I did this data extraction in two different steps:

1. I used Selenium and the advanced search tools from Youtube to obtain videos IDs.

2. I used the Youtube API to obtain data from this videos IDs. Info about this API:
    - Base URL used: [Youtube API](https://www.googleapis.com/youtube/v3/videos)
    - Parameters:
        - Part: snippet, contentDetails, statistics. It provides detailed information about a video such views, comments, likes, date of publication or length of the video.
        - id: video_id. The alphanumeric code used in the URL to identify a video.
        - key: token.

All these datasets have allowed me to create a database in MySQL in order to make the video games analysis.

![](../videogames_industry/images/diagram.png)


## Data Analysis

As explained at the beginning, I am going to analyze these data from two different perspectives:

- The Jupyter Notebook: **"Overview_Analysis"**, which makes a general analyisis of the video games industry.

- The Jupyter Notebook: **"one_game_analysis"**,
which compare a single video game with its peers.

## Results

Video games industry has reached a peak in 2021 and maybe it's time for VR to take the lead and boost this industry.


## Files structure

- Data: all data obtained in the data acquisition process.
- Images: images used in this readme.
- Notebooks: all code used in the data wrangling, data cleaning, data analysis and data visualization process.
- sql: database creation and some queries.
- src: functions created to use in the notebooks files.

## Libraries

[Pandas](https://pandas.pydata.org/)
[Numpy](https://numpy.org/doc/)
[Seaborn](https://seaborn.pydata.org/index.html)
[Matplotlib](https://matplotlib.org/3.1.1/contents.html)
[Requests](https://pypi.org/project/requests/2.7.0/)
[SQL Alchemy](https://www.sqlalchemy.org/)
[Selenium](https://www.selenium.dev/)