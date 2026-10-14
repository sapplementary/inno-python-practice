-- the 1st test query
select r.id, r.name, count(s.id) as count_students
from rooms r
left join students s on s.room_id = r.id 
group by r.id, r.name

-- the 2nd test query
select r.id , r.name, avg(extract(year from age(s.birthday))) as avg_age
from rooms r
join students s on s.room_id = r.id
group by r.id , r.name

--the 3rd test query
select r.id , r.name, max(extract(year from age(s.birthday)))
					- min(extract(year from age(s.birthday))) as age_diff
from rooms r
join students s on s.room_id = r.id
group by r.id , r.name
limit 5

-- the 4th test query
select r.id, r.name
from rooms r 
join students s ON s.room_id = r.id
group by r.id, r.name
having COUNT(DISTINCT s.sex) > 1