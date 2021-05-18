import random
import string
import variable


# create a class named user for interactions
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


# get how many row the table have
def getRowCount(connection, tablename):
    # create a cursor
    dbcur = connection.cursor()
    # execute the SQL statment to get every entry of a specific table
    dbcur.execute("SELECT * FROM " + tablename)
    # get everything
    dbcur.fetchall()
    # count everything
    rowcount = dbcur.rowcount
    # return the counter
    return rowcount


# function to get a user from the DB
def getUsersFromDB(connection, wherecondition):
    dbcur = connection.cursor()

    dbcur.execute("SELECT * FROM users where " + wherecondition)
    record = dbcur.fetchall()
    dbcur.close()

    return record


# fill a global variable with every user registered in the DB
def fillArray(connection):
    # get a integer from counting the rows and add 3 just to be sure everyone is counted
    rowCount = getRowCount(connection, "users") + 3
    # get the last user id
    lastUserID = getlastUserID(connection)
    # add the last user id to the row count (just to be sure)
    rowCount = lastUserID + rowCount

    i = lastUserID - 1

    # iterate through all the possible users
    for i in range(rowCount):
        # convert the integer to a string for the SQL statment
        n = str(i)
        # get the user from the DB using the iterated integer
        values = getUsersFromDB(connection, "userID = " + n)

        # get every value from this user
        for row in values:

            userID = row[0]
            username = row[1]
            password = row[2]

            # if the user is not in the array append the user object
            if not userID in variable.authentificatedUsers and not username in variable.authentificatedUsers and not password in variable.authentificatedUsers:
                variable.authentificatedUsers.append(User(id=userID, username=username, password=password))


# no comments needed
def getlastUserID(connection):
    for i in range(1000000):
        n = str(i)

        values = getUsersFromDB(connection, "userID = " + n)

        for row in values:
            userID = row[0]

            if userID:
                return int(userID)


# function to check if a specific invitation exist
def doesInvitationExist(connection, invitationcode):
    dbcur = connection.cursor()

    dbcur.execute("SELECT * FROM invitation where inKey = " + "'" + invitationcode + "'")

    record = dbcur.fetchall()

    dbcur.close()

    # iterate trough the SQL answer and check if it exist
    for row in record:
        invitation = row[1]

        if invitation:
            return True
    return False


# function to check if the username is already taken
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


# function to add the user to the DB
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


# function to create new invitations inside the admin menu
def invGen(connection, amount):
    amount = int(amount)

    # lag and load reducing option max 100 invs
    if amount > 100:
        amount = 100

    variable.invites = []

    # for every request key generate a invitation
    for i in range(amount):
        key = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in
            range(32))
        dbcur = connection.cursor()

        dbcur.execute("INSERT INTO invitation (inKey) VALUES ('" + key + "');")

        connection.commit()
        dbcur.close()
        variable.invites.append(key)
