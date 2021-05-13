# SDN python
Python SDN control center with Flask.

Flask webserver with Jinja2 object paired with the beautiful bootstrap v5 framework.
This SDN control center is a school project and is not a real thing.
It should simulate how it could look and "feel".

The control center uses pre defined buttons,
to control the cisco sandbox SD-Wan environment using the rest-API.

The whole project take securtity very seriously, thats why SQL injections are not possible and 
passwords get stored in a md5 hash. Neither me or anyone else have access to the password in your DB.

As you probably seen many ressource references (mainly in the html part) going to a website <a href="https://wycofane.de">Wycofane.de</a> that's my personal
project and is not finished yet. The website is similar built, but not communication with cisco. <a href="https://wycofane.de">Wycofane.de</a> communicate with the 
proxmox rest-API.



</br>
Dependencies:

> Flask </br>
> Jinja2 </br>
> mysql-connector-python



## The SQL syntax for creating the database tables:
```
create table users (userID int AUTO_INCREMENT, username varchar(255) Not null, password char(32) Not null, status int, primary key (userID));

create table invitation (invID int AUTO_INCREMENT, inKey char(32) not null, primary key (invID));
```



