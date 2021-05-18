# SDN python
Python SDN control center with Flask. Mainly build for the GUI.

Flask web server with Jinja2 object paired with the beautiful bootstrap v5 framework.
This SDN control center is a school project and is not a real thing.
It should simulate how it could look and "feel".

The control center uses pre-defined buttons,
to control the Cisco sandbox SD-Wan environment using the rest-API.

The whole project takes security very seriously, that's why SQL injections are not possible and 
passwords get stored in a md5 hash. Neither me nor anyone else has access to the password in your DB.

As you probably have seen many resource references (mainly in the HTML part) go to a website named <a href="https://wycofane.de">Wycofane.de</a>. That's my personal
project and is not finished yet. The website is built similar, but there is no communication with Cisco. <a href="https://wycofane.de">Wycofane.de</a> communicates with the 
Proxmox rest-API.


</br>
You have to create a file named "sensitiveData.py" in order to use this software.

Layout sensitiveData.py:


```
dbUsername = "user"
dbPassword = "password"
dbHostIP = "i.p.a.ddress"
db = "users"
vmanage_ip = "sandboxIPorURL"
username = "devnetuser"
password = "CiscoPW"
adminUsername = "admin"
```

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



