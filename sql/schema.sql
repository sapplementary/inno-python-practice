create table rooms (
	id int primary key,
	name varchar(50) not null 
)

create table students(
	id int primary key,
	name varchar(120) not null,
	birthday date not null,
	sex char(1) not null check (sex in ('M', 'F')),
	room_id int not null references rooms(id)
)
