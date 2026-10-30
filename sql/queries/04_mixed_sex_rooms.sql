SELECT   r.id,
         r.name
FROM     rooms r
         JOIN students s
         ON s.room_id = r.id
GROUP BY r.id,
         r.name
HAVING   Count(DISTINCT s.sex) > 1