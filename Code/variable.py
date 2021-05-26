import sensitiveData as sd
import mysql.connector
from logger import logger
import sys

name = "anon"
authentificatedUsers = []
secretkey = "sLWqVgyq8ZEQMK0AdaQrBcHlw36fo6K23f83zxbwsiYetQQzbbeqJdAXg3JJz5Mz2vepPS8lM6g2CLapqpPbMv56K5R3PROJ2iXa9XzwiqunRxRsSIppmqZ0Q6JMg"
dbUsername = sd.dbUsername
dbPassword = sd.dbPassword
dbHostIP = sd.dbHostIP
db = sd.db
deviceData = []
site = """"""
controlpanel = """"""
border = """"""
invites = []
string = ""


def createConnection():
    try:
        connection = mysql.connector.connect(host=dbHostIP, database=db, user=dbUsername, password=dbPassword)
        conTest = connection.is_connected()
        if conTest:
            return connection
        else:
            connection = mysql.connector.connect(host=dbHostIP, database=db, user=dbUsername, password=dbPassword)
            return connection
    except mysql.connector.Error as e:
        logger("failed because of " + str(e) + " trying again ...")
        try:
            connection = mysql.connector.connect(host=dbHostIP, database=db, user=dbUsername, password=dbPassword)
            return connection
        except mysql.connector.Error as e:
            logger("failed twice now because of " + str(e) + " shutting down")
            print("Error MYSQL check log!")
            sys.exit(1)
