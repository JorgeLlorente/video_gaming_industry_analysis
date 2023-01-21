CREATE DATABASE videogames_industry;

USE videogames_industry;

DROP TABLE videojuegos;

CREATE TABLE videojuegos (
	videojuego_id VARCHAR(255),
    platform VARCHAR(255),
    release_date DATE,
    summary VARCHAR(10000),
    meta_score DECIMAL(5,2),
    user_review DECIMAL(5,2),
    PRIMARY KEY (videojuego_id)
);

DROP TABLE torneos;

CREATE TABLE torneos (
	videojuego_id VARCHAR (255),
    posicion INT,
    dinero DECIMAL (20, 2),
    jugadores INT,
    torneos INT,
    fecha DATE
);

DROP TABLE generos;

CREATE TABLE generos (
	videojuego_id VARCHAR (255),
    genero VARCHAR (255)
);
    
DROP TABLE info_general;

CREATE TABLE info_general (
	videojuego_id VARCHAR (255),
    developer VARCHAR (255),
    jugadores VARCHAR (255),
    rating VARCHAR(5)
);

DROP TABLE twitch;

CREATE TABLE twitch (
	videojuego_id VARCHAR (255),
    watch_time_hours VARCHAR (255),
    stream_time_hours INT,
    peak_viewers INT,
    peak_channels INT,
    streamers INT,
    average_viewers INT,
    average_channels INT,
    average_viewer_ratio INT,
    fecha DATE
);

DROP TABLE youtube;

CREATE TABLE youtube (
    publishedat DATE,
    channeltitle VARCHAR (255),
    duration INT,
    viewcount INT,
    likecount INT,
    commentcount INT,
    juego VARCHAR (255)
);