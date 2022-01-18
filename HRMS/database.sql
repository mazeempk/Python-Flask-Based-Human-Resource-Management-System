CREATE database HR;
use HR;
create table regTable(userID int NOT NULL AUTO_INCREMENT,firstName varchar(40),lastName varchar(40),age int,username varchar(30),email varchar(80), password varchar(30),PRIMARY KEY (userID));
select * from regTable;
SELECT COUNT(*) FROM regtable;
drop table jobsTable;  
create table jobsTable(jobID int NOT NULL AUTO_INCREMENT,title varchar(255) NOT NULL,catagory varchar(255) NOT NULL,type varchar(255) NOT NULL,salary varchar(30),expr varchar(255), country varchar(255),PRIMARY KEY (jobID));
select * from jobsTable;

create table applicantsTable(formID int NOT NULL AUTO_INCREMENT PRIMARY KEY,jobID int,name varchar(255) NOT NULL,email varchar(255) NOT NULL,phone varchar(255) NOT NULL,cnic varchar(30),job varchar(110),foreign key(jobID) references jobsTable(jobID));
select * from applicantsTable;
drop table applicantstable;

create table employeesTable(empID int NOT NULL AUTO_INCREMENT PRIMARY KEY,name varchar(255) NOT NULL,username varchar(255),email varchar(255) NOT NULL unique,cnic varchar(30), dept varchar(255) NOT NULL, typee varchar(255) NOT NULL);
select * from employeesTable;

create table payroll(payID int NOT NULL AUTO_INCREMENT PRIMARY KEY ,username varchar(255),email varchar(255), salary int, timee date);
select * from payroll;
drop table payroll;

