SELECT   r.id,
         r.name,
         Count(s.id) AS count_students
FROM     rooms r
         LEFT JOIN students s
         ON s.room_id = r.id
GROUP BY r.id,
         r.name
ORDER BY r.id;