select *from account

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

alter table product rename quantity to price$
select *from product

