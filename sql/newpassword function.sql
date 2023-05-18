 create or replace function newpassword(newid integer,pass2 text)
 returns void
 language plpgsql
 as $$
 begin
 update account set pass=pass2 where id=newid;
 end;
 $$
 
 select *From account