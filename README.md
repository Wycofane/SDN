# SDN
Python SDN Control Center with Flask


## The SQL Commandy for creating the Databse Table:
```
create table users (userID int AUTO_INCREMENT, username varchar(255) Not null, password char(32) Not null, status int, primary key (userID));

create table invitation (invID int AUTO_INCREMENT, inKey char(32) not null, primary key (invID));
```
