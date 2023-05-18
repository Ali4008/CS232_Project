create or replace function totalaccounts()
returns int
language plpgsql
as 
$$
declare
total integer;
begin
select count(*) into total from account;
return total;
end;
$$

select totalaccounts()