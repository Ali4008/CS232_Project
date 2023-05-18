ALTER TABLE product
DROP CONSTRAINT product_id_fkey,
ADD CONSTRAINT fk_account_id
FOREIGN KEY (id)
REFERENCES account(id)
ON DELETE CASCADE;

select *From account
select *from product

create table deleted(
username text,
deltime timestamp
)

create or replace function deletedaccount()
 returns trigger
 language plpgsql
 as $$
 begin
 insert into deleted(username,deltime) values(old.username,now());
 return old;
 end;
 $$
 
 create trigger deleted
 after delete on account 
 for each row
 execute function deletedaccount()
  delete from account where id=8
  select *From deleted
 