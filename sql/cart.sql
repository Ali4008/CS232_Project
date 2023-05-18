create table cart(
 id serial,
	foreign key(id)
	references account(id),
	price integer,
	image text
)

select *from account