SELECT   r.id,
         r.name,
         ROUND((MAX(s.birthday) - MIN(s.birthday)) / 365.25, 2)::float AS age_diff_years
FROM     rooms r
         JOIN students s
         ON s.room_id = r.id
GROUP BY r.id,
         r.name
LIMIT 5