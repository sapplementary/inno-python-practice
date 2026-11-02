WITH ages AS (
    SELECT room_id,
           EXTRACT(YEAR FROM AGE(CURRENT_DATE, birthday))::int AS age
    FROM students
)
SELECT r.id,
       r.name,
       ROUND(AVG(a.age), 2)::float AS avg_age_years
FROM rooms r
JOIN ages a ON a.room_id = r.id
GROUP BY r.id, r.name
ORDER BY AVG(a.age) ASC, r.id
LIMIT 5;