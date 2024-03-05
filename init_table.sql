
create database comp6841db;

\c comp6841db;

create table person (
    id serial not null primary key, 
    name varchar(64) not null, 
    email varchar(64) not null unique, 
    password varchar(64) not null
);

create table course (
    id serial not null primary key, 
    course_name varchar(64) not null unique,
    description varchar(128)
);

insert into course values (1,'COMP9900 project', 'project on web application'),
                        (2, 'COMP9337 fixed and wireless network', 'a course about cybersecurity'),
                        (3, 'COMP6841 network security extension', 'introduction to computer security and cyber crime'),
                        (4, 'COMP6991 rust programming', 'solve modern problems using rust'),
                        (5, 'COMP9313 big data management', 'hadoop'),
                        (6, 'COMP9331 network application', 'a course about network application'),
                        (7, 'COMP9021 principles of programming', 'this is a first programming course');

create table prerequsite(
    pre_id int references course(id) on delete cascade, 
    course_id int references course(id)
);

insert into prerequsite values (7, 4), 
                            (7, 3), 
                            (7, 2),
                            (6, 2),
                            (5, 1),
                            (6, 1),
                            (7, 1);

create table student_course(
    student_id int references person(id) on delete cascade, 
    course_id int references course(id) on delete cascade,
    status bool not null
);

create table top_secret (
    admin_name varchar(64), 
    password varchar(64)
);

insert into top_secret values ('admin', 'aswd');

create table course_comment (
    course_id integer references course(id), 
    comment varchar(256) not null
);
