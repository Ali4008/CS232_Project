
select *From product
ALTER TABLE product ADD PRIMARY KEY (prodid,image);
select *from cart
select *from currentuser
select *from account

create table orders(
oid serial,
id serial,
foreign key(id)
references account(id),
price integer	
)
drop table orders

select *from account
select id from cart where id =(select id from account inner join currentuser on account.username=currentuser.username)
select string_agg(image,',') from cart where id =(select id from account inner join currentuser on account.username=currentuser.username)

select *From orders
select *from cart
select *From account