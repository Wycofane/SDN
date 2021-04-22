from mysql.connector import Error
import variable


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


def getRowCount(connection, tablename):
    dbcur = connection.cursor()

    dbcur.execute("SELECT * FROM " + tablename)

    dbcur.fetchall()

    rowcount = dbcur.rowcount

    return rowcount


def getUsersFromDB(connection, wherecondition):
    dbcur = connection.cursor()

    dbcur.execute("SELECT * FROM users where " + wherecondition)

    record = dbcur.fetchall()

    dbcur.close()

    return record


def fillArray(connection):
    rowCount = getRowCount(connection, "users") + 3

    lastUserID = getlastUserID(connection)

    rowCount = lastUserID + rowCount

    i = lastUserID - 1

    for i in range(rowCount):

        n = str(i)

        values = getUsersFromDB(connection, "userID = " + n)

        for row in values:

            userID = row[0]

            username = row[1]

            password = row[2]

            if not userID in variable.authentificatedUsers and not username in variable.authentificatedUsers and not password in variable.authentificatedUsers:
                variable.authentificatedUsers.append(User(id=userID, username=username, password=password))



def getlastUserID(connection):
    for i in range(1000000):

        n = str(i)

        values = getUsersFromDB(connection, "userID = " + n)

        for row in values:
            userID = row[0]

            if userID:
                return int(userID)


def doesInvitationExist(connection, invitationcode):
    dbcur = connection.cursor()

    dbcur.execute("SELECT * FROM invitation where inKey = " + "'" + invitationcode + "'")

    record = dbcur.fetchall()

    dbcur.close()

    for row in record:

        invitation = row[1]

        if invitation:
            return True

    return False


def doesUsernameAlreadyExist(connection, username):
    dbcur = connection.cursor()

    dbcur.execute("SELECT * FROM users where username = " + "'" + username + "'")

    record = dbcur.fetchall()

    dbcur.close()

    for row in record:

        username = row[1]

        if username:
            return False

    return True


def deleteInvitation(connection, invitationcode):
    dbcur = connection.cursor()

    dbcur.execute("DELETE FROM invitation where inKey = '" + invitationcode + "'")

    connection.commit()

    dbcur.close()


def insertValueIntoUser(connection, username, password):
    dbcur = connection.cursor()

    dbcur.execute(
        "INSERT INTO users (username,password,status) VALUES ('" + username + "','" + password + "'," + str(1) + ");")

    connection.commit()

    dbcur.close()


def getUser(connection, username):
    dbcur = connection.cursor()

    dbcur.execute("SELECT * FROM users where username = " + "'" + username + "'")

    record = dbcur.fetchall()

    dbcur.close()

    return record
