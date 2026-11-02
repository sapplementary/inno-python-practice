WITH ages AS (
    SELECT room_id,
           birthday,
           EXTRACT(YEAR FROM AGE(CURRENT_DATE, birthday))::int AS age
    FROM students
)
SELECT r.id,
       r.name,
       MAX(a.age) - MIN(a.age) AS age_diff_years
FROM rooms r
JOIN ages a ON a.room_id = r.id
GROUP BY r.id, r.name
ORDER BY age_diff_years DESC,
         MAX(a.birthday) - MIN(a.birthday) DESC,
         r.id
LIMIT 5;