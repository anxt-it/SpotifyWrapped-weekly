-- name: top_songs
select track_name, artist_name, count(*) as count_track, SUM(duration_ms) / 6000.0
from listening_history
where played_at >= date('now', '-7 days')
group by track_id
order by count_track desc
limit 5


-- name: top_artists
select artist_name, count(*) as plays, sum(duration_ms) / 6000 as minutes_with_artist
from listening_history
where played_at >= date('now', '-7 days')
group by 1
order by 2 desc


-- name: total_time
select sum(duration_ms) / 60000.0 as minutes_played
from listening_history
where played_at >= date('now', '-7 days')
