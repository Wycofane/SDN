import hashlib
from flask import Flask, render_template, redirect, url_for, request, g, session
import dbUtility as dbU
import initialize
import jsonHelper
import variable
from logger import logger
from mainUtility import addDevicesToGui, buildSiteCP
from sensitiveData import adminUsername

# Initialize a database connection
connection = variable.createConnection()

# Initialize the Flask APP
app = Flask(__name__)

# Secret app key for Session usage
app.secret_key = variable.secretkey


# Default Index route site
@app.route('/')
def index():
    # Check if the user is in the global context logged in if not redirect to the main page
    if g.user:
        return redirect(url_for('home'))

    return render_template('index.html')


@app.before_request
def before_request():
    g.user = None

    if 'username' in session:
        if len(variable.authentificatedUsers) > 0:
            for x in variable.authentificatedUsers:
                if x.username == session['username']:
                    user = x
                    g.user = user


@app.route('/home')
def home():
    # Check if the user is in the global context logged in if not redirect to the main page
    if not g.user:
        return redirect(url_for('index'))

    if g.user.username == adminUsername:
        return redirect(url_for('homeAdmin'))

    return render_template('home.html')


@app.route('/homeAdmin', methods=['GET', 'POST'])
def homeAdmin():
    error = None

    # check if the user is in the global context logged in if not redirect to the main page
    if not g.user:
        return redirect(url_for('index'))

    # if the user press the button with the type "submit" then do smth
    if request.method == 'POST':
        amount = request.form['amount']

        if amount == "0":
            error = "Anzahl zu klein"
        else:
            dbU.invGen(connection, amount)

            variable.string = ""

            for invite in variable.invites:
                variable.string = variable.string + invite + "\n"
            error = variable.string

    # check if the user is an admin if not redirect to the normal ladning page
    if g.user.username != adminUsername:
        render_template('home.html')

    # render the amdin menu
    return render_template('Adminhome.html', error=error)


# Default explanations site
@app.route('/was-ist-das')
def help():
    return render_template('help.html')


@app.errorhandler(403)
def forbidden(e):
    # Check if the user is in the global context logged in if yes redirect to the page but with changed layout
    if g.user:
        return render_template('403_li.html'), 403

    return render_template('403.html'), 403


# Error handler sites
@app.errorhandler(404)
def page_not_found(e):
    # Check if the user is in the global context logged in if yes redirect to the page but with changed layout
    if g.user:
        return render_template('404_li.html'), 404

    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    # Check if the user is in the global context logged in if yes redirect to the page but with changed layout
    if g.user:
        return render_template('500_li.html'), 500

    return render_template('500.html'), 500


@app.route('/login', methods=['GET', 'POST'])
def welcome():
    error = None

    if g.user:
        return redirect(url_for('home'))

    if request.method == 'POST':

        # remove the browser from the session
        session.pop('username', None)

        # add every user registered to an a array (maybe not scale friendly)
        dbU.fillArray(connection)

        # request the data typed in
        usernameInput = request.form['username']
        passwordInput = request.form['password']

        # convert the password to a md5 hash
        passwordInput = hashlib.md5(passwordInput.encode()).hexdigest()

        # get the user from the db
        values = dbU.getUser(connection, usernameInput)

        # iterate through the user
        for row in values:

            # get the data from the user (db)object
            username = row[1]
            password = row[2]

            # check if the datas are the same (basic login stuff)
            if password == passwordInput and username == usernameInput:

                # if yes add the user to the session
                session['username'] = usernameInput

                # check if it is the admin
                if usernameInput == adminUsername:
                    return redirect(url_for('homeAdmin'))
                else:
                    return redirect(url_for('home'))

            else:
                error = 'Falsche Login Daten bitte erneut versuchen!'
        error = 'Falsche login Daten bitte erneut versuchen!'

    return render_template("loginform.html", error=error)  # render a templates


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    # Check if the user is in the global context logged in if not redirect to the main page
    if g.user:
        return redirect(url_for('home'))

    return redirect(url_for('index'))


# Simple Signup form backend
@app.route('/signup', methods=['GET', 'POST'])
def register():
    error = None

    # Check if the user is in the global context logged in if yes redirect to the ladning page
    if g.user:
        return redirect(url_for('home'))

    # If the User Post the filled form
    if request.method == 'POST':

        # Get the Username from the form
        usernameInput = request.form['username']

        # Get the password from the form
        passwordInput = request.form['password']

        # Get the repeated password from the form
        repeatpasswordInput = request.form['repeatpassword']

        # Get the invitation from the form
        invitationInput = request.form['invitation']

        # First check: are the both passwords the same
        if passwordInput != repeatpasswordInput:
            error = "ERROR: Deine Passwörter müssen übereinstimmen"

        # Ask the DB if the username is already taken
        if not dbU.doesUsernameAlreadyExist(connection, usernameInput):
            error = "ERROR: Benutzername existiert bereits"

        # Check if the invitation code is an actually invitation
        if not dbU.doesInvitationExist(connection, invitationInput):
            error = "ERROR: Einladungscode existiert nicht"

        # Check if User is just dumb or trying to the the errorhandling
        if not usernameInput or not passwordInput or not repeatpasswordInput or not invitationInput:
            error = "ERROR: Bitte das Formular ausfüllen"

        # The password has to be at least 8 digits long
        if len(passwordInput) < 8:
            error = "ERROR: Dein Passwort muss 8 Zeichen lang sein oder länger"

        # Checking for non aplhanumeric chars
        if any(not c.isalnum() for c in usernameInput):
            error = "ERROR: Bitte nur Alpanumerische Zeichen"

        # Check if the Username is longer then 4 digits
        if not len(usernameInput) >= 4:
            error = "ERROR: Dein Benutzername muss mindestens 4 Zeichen lang sein"

        # If all checks are passed then the Account gets created and the password get stored in the DB transformed to a md5 hash
        if len(usernameInput) >= 4 and passwordInput == repeatpasswordInput and dbU.doesUsernameAlreadyExist(connection,
                                                                                                             usernameInput) \
                and dbU.doesInvitationExist(connection, invitationInput) and \
                len(passwordInput) >= 8 and not any(not c.isalnum() for c in usernameInput):
            error = "Dein Account wurde erstellt, logge dich nun ein"

            # convert password to a md5 hash
            passwordInput = hashlib.md5(passwordInput.encode()).hexdigest()

            # add the user to the db
            dbU.insertValueIntoUser(connection, usernameInput, passwordInput)

            # delete the invitation
            dbU.deleteInvitation(connection, invitationInput)

    return render_template("register.html", error=error)  # render a templates


@app.route('/logout')
def logout():
    # Check if the user is in the global context logged in if not redirect to the main page
    if not g.user:
        return redirect(url_for('index'))

    # Remove the user from the Session
    session.pop('username')

    # Redirect to the main page
    return redirect(url_for('index'))


@app.route('/controlpanelAction', methods=['GET', 'POST'])
def controlpanelAction():

    # Check if the user is in the global context logged in if not redirect to the main page
    if not g.user:
        return redirect(url_for('index'))

    # get the actionID from the url
    ActionId = request.args['id']

    # for loop helper integer
    i = 1

    # iterate trhough every device that cisco sended us
    for value in variable.deviceData['data']:

        # acquire the values of the current device
        hostname = value['host-name']
        uuid = value['uuid']
        ip = value['system-ip']

        # if it is the right device build the payload and send it
        if str(i) == ActionId:

            # get the payload build as a json
            payload = jsonHelper.payloadBuilderReboot(hostname, ip, uuid)

            # execute the post request "reboot"
            logger(initialize.post_request("device/action/reboot", payload))
        i = i + 1

    return redirect(url_for("controlpanel"))


# Controlpanel
@app.route('/controlpanel', methods=['GET', 'POST'])
def controlpanel():
    error = None

    # Check if the user is in the global context logged in if not redirect to the main page
    if not g.user:
        return redirect(url_for('index'))

    # build the dynamic site
    buildSiteCP()

    # render the dynamic page
    return variable.controlpanel


# small gimick just to populate the navbar
@app.route('/bonus', methods=['GET', 'POST'])
def bonus():
    # Check if the user is in the global context logged in if not redirect to the main page
    if not g.user:
        return redirect(url_for('index'))

    return render_template('bonus.html')


# "Main function" start of the Flask APP
if __name__ == '__main__':
    logger('Startup SDN Controller')

    # add the devices of the sandbox dynamically
    addDevicesToGui()

    # Run the flask server accessible in the LAN
    app.run(host="0.0.0.0", port=80)

