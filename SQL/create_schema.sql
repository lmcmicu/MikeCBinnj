drop table if exists lunch_expenses;
drop table if exists employee;

create table employee (
	   id smallserial,
	   uname char(4) not null,
	   passwd varchar(72),
	   fname varchar(30),
	   lname varchar(30),
	   constraint pk_emp_id primary key (id),
	   constraint unique_emp_uname unique (uname)	   
);

create table lunch_expenses (
	   emp_id smallint,
	   lunch_date date,
	   amount numeric(6,2),
	   constraint pk_lunch_expenses primary key (emp_id, lunch_date),
	   constraint fk_lunch_expenses_1 foreign key (emp_id) references employee (id)
);
