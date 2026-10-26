SELECT   r.id,
         r.name,
         ROUND(AVG(CURRENT_DATE - s.birthday) / 365.25, 2)::float AS avg_age_years
FROM     rooms r
         JOIN students s
         ON s.room_id = r.id
GROUP BY r.id,
         r.name
LIMIT 5