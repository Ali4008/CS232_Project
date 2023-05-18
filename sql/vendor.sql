

select *from account
select *from product

create table vendor(
username varchar(30),
foreign key(username)
references account(username),
prodname text	
)

select *from vendor


create or replace procedure vendors(username text,prodname text)
language plpgsql
as $$
begin
insert into vendor values(username,prodname);
end;$$