import sensitiveData as sd
import mysql.connector

name = "anon"
authentificatedUsers = []
secretkey = "sLWqVgyq8ZEQMK0AdaQrBcHlw36fo6K23f83zxbwsiYetQQzbbeqJdAXg3JJz5Mz2vepPS8lM6g2CLapqpPbMv56K5R3PROJ2iXa9XzwiqunRxRsSIppmqZ0Q6JMg"
dbUsername = sd.dbUsername
dbPassword = sd.dbPassword
dbHostIP = sd.dbHostIP
db = sd.db
connection = mysql.connector.connect(host=dbHostIP, database=db, user=dbUsername, password=dbPassword)
deviceData = []
site = """"""
controlpanel = """"""
border = """"""
