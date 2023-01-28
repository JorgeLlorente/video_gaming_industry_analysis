SELECT videogame_id, genero, meta_score
FROM generos
INNER JOIN videogames_industry.videogames_unique ON generos.videojuego_id = videogames_unique.videogame_id
WHERE genero = 'Role-Playing';

SELECT videogame_id, watch_time_hours, viewcount, publishedat, fecha
FROM videogames_unique
INNER JOIN youtube ON videogames_unique.videogame_id = youtube.juego
INNER JOIN twitch ON videogames_unique.videogame_id = twitch.videojuego_id;

SELECT videogame_id, genre, release_date
FROM videogames_unique
INNER JOIN genres ON videogames_unique.videogame_id = genres.videojuego_id;

DELETE
FROM youtube
WHERE fecha < "2013-01-01" AND videogame_id = "Call of Duty: Warzone";

SELECT videogames_unique.videogame_id, videogames_unique. release_date, platform, meta_score, user_review
FROM platforms
INNER JOIN videogames_unique ON platforms.videogame_id = videogames_unique.videogame_id;

SELECT genres.videogame_id, genre, watch_time_hours, fecha
FROM genres
LEFT JOIN twitch ON genres.videogame_id = twitch.videogame_id
WHERE genre = "Action";

SELECT videogames_unique.videogame_id, user_review, SUM(viewcount) AS visitas
FROM videogames_unique
RIGHT JOIN youtube ON videogames_unique.videogame_id =  youtube.videogame_id
WHERE viewcount > 100000
GROUP BY videogame_id
ORDER BY visitas DESC;

SELECT twitch.videogame_id, genre, watch_time_hours
FROM twitch
INNER JOIN genres ON twitch.videogame_id = genres.videogame_id
ORDER BY watch_time_hours DESC
LIMIT 10;


SELECT twitch.videogame_id, jugadores, rating, MAX(watch_time_hours)
FROM twitch
INNER JOIN info_general ON twitch.videogame_id = info_general.videogame_id;

SELECT twitch.videogame_id, dinero, torneos, MAX(watch_time_hours)
FROM twitch
INNER JOIN torneos ON twitch.videogame_id = torneos.videogame_id;


