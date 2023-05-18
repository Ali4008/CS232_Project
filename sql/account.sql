select *from account
drop table account
create table account(
id serial primary key,
username varchar(30),
pass varchar(30),
email varchar(40)	
)