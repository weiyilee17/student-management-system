# Commands

### Login
`mysql -u ${username} -p`

to enter MySQL. Then type in the password.
### Show databases

`SHOW DATABASES;`

All commands ends with ;

### Create database

`CREATE DATABASE school;`

Use command line to create the database once, and use python code to interact with the database for all other requests.

### Show tables

`SHOW TABLES FROM school;`

### Change databases

`USE school;`

### Create tables

`CREATE TABLE students(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(255),
course VARCHAR(255),
mobile VARCHAR(255)
);`

Press enter for multiple lines. As long as you don't type ; you can keep line breaking.
Column names should be in lower case.

Primary keys are used to uniquely identify a row.
Varchar are strings

Can't be executed if database isn't selected first(have to use `USE ${database}` to change database)

### Show all data in table

`SELECT * FROM students;`

### Add entries

`INSERT INTO students (name, course, mobile)
VALUES ("Emma Pike", "Math", "12345");`

### Exit

`Exit;`

