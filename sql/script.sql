begin;



create table if not exists employees_temp
(
    name       text,
    age        int,
    email      text,
    department text,
    salary     bigint
);

create table if not exists employees
(
    name       text,
    age        int,
    email      text,
    department text,
    salary     bigint,
    primary key (name, email)
    );

\copy employees_temp(name, age, email, department, salary) from 'employees.csv' with delimiter ',' csv header;

insert into employees (name, age, email, department, salary)
select name, age, email, department, salary from employees_temp
    on conflict (name, email) do nothing;

drop table employees_temp;

commit;
