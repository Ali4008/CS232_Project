select *from account
select *from product
select *from vendor

drop table vendor
drop table product
drop table cart
drop table account
create table account(
id serial ,
username varchar(30),
pass varchar(30),
email varchar(40),
primary key(id,username)
)

ALTER TABLE account ADD CONSTRAINT account_number_unique UNIQUE (id);
ALTER TABLE account ADD CONSTRAINT username_unique UNIQUE (username);
create table product(
prodid serial primary key,
prodname text,
quantity integer,
description text,
image character(100),
id serial,
foreign key(id)
references account(id)

)

alter table product rename quantity to price