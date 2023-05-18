select *From account
select *From currentuser
drop table details
create table details(
	id serial primary key,
username character(30),
foreign key(username)
	references account(username),
	address text,
	city text,
	phone bigint

)

select *From details