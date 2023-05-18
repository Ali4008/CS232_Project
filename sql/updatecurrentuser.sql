create or replace procedure update_current_user(usern text)
language plpgsql
as
$$
begin
update currentuser
set username = usern
where uid = 1;
end;
$$


select * from cart;

alter table account add constraint usernameunique unique(username)
select *from account
insert into cart values('1', '10', 'shirt1.jpeg');

select *from currentuser