# SDN python
Python SDN control center with Flask.

Flask webserver with Jinja2 object paired with the beautiful Bootstrap v5 Framework.
This SDN control center is a shool project, and is not a real thing.
It should simulate how it could look and "feel".
</br>
The control center uses pre defined buttons,
to control the cisco sandbox SD-Wan envoriment, using a Rest-API by cisco.



</br>
Dependencies:
```
Flask
Jinja2
mysql-connector-python
```
```


## The SQL syntax for creating the database tables:
```
create table users (userID int AUTO_INCREMENT, username varchar(255) Not null, password char(32) Not null, status int, primary key (userID));

create table invitation (invID int AUTO_INCREMENT, inKey char(32) not null, primary key (invID));
```



