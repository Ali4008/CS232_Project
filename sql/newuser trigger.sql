create table newuser(
userid serial primary key,	
username character(30)
)
create or replace function updatenewuser()
returns trigger
language plpgsql
as $$
begin
insert into newuser(username) values(new.username);
return new;
end;
$$
select * from account
select *from newuser
select *from product
create trigger newuser
after insert on account
for each row
execute procedure updatenewuser()
