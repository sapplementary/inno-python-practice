-- the 1st test query
SELECT   r.id,
         r.name,
         Count(s.id) AS count_students
FROM     rooms r
         LEFT JOIN students s
         ON s.room_id = r.id
GROUP BY r.id,
         r.name
order by r.id;

-- the 2nd test query

SELECT   r.id,
         r.name,
         ROUND(AVG(CURRENT_DATE - s.birthday) / 365.25, 2) AS avg_age_years
FROM     rooms r
         JOIN students s
         ON s.room_id = r.id
GROUP BY r.id,
         r.name
LIMIT 5;

--the 3rd test query

SELECT   r.id,
         r.name,
         (MAX(s.birthday) - MIN(s.birthday)) / 365.25, 2 AS age_diff_years
FROM     rooms r
         JOIN students s
         ON s.room_id = r.id
GROUP BY r.id,
         r.name
LIMIT 5;

-- the 4th test query

SELECT   r.id,
         r.name
FROM     rooms r
         JOIN students s
         ON s.room_id = r.id
GROUP BY r.id,
         r.name
HAVING   Count(DISTINCT s.sex) > 1;
