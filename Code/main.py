import hashlib
from flask import Flask, render_template, redirect, url_for, request, make_response, g, session, Response
import initialize
import dbUtility as dbU
import variable
import sensitiveData as sd
import requests

# Variable block


connection = variable.connection

# Initialize the Flask APP
app = Flask(__name__)

# Secret App key for Session usage
app.secret_key = variable.secretkey


# Default Index route site
@app.route('/')
def index():
    return render_template('index.html')


@app.before_request
def before_request():
    g.user = None

    if 'username' in session:
        if len(variable.authentificatedUsers) > 0:
            print(variable.authentificatedUsers)
            for x in variable.authentificatedUsers:
                if x.username == session['username']:
                    user = x
                    g.user = user


@app.route('/home')
def home():
    if not g.user:
        return redirect(url_for('index'))

    return render_template('home.html')


# Default explanations site
@app.route('/was-ist-das')
def help():
    return render_template('help.html')


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


# Error handler sites
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/login', methods=['GET', 'POST'])
def welcome():
    error = None

    if g.user:
        return redirect(url_for('home'))

    if request.method == 'POST':

        session.pop('username', None)

        dbU.fillArray(connection)

        usernameInput = request.form['username']

        passwordInput = request.form['password']

        passwordInput = hashlib.md5(passwordInput.encode()).hexdigest()

        values = dbU.getUser(connection, usernameInput)

        for row in values:

            username = row[1]

            password = row[2]

            status = row[3]

            if password == passwordInput and username == usernameInput:

                resp = make_response(redirect(url_for('home')))

                session['username'] = usernameInput

                return resp

            else:
                error = 'Invalid Credentials. Please try again.'
        error = 'Invalid Credentials. Please try again.'

    return render_template("loginform.html", error=error)  # render a templates


@app.route('/auth', methods=['GET', 'POST'])
def auth():

    if g.user:
        return redirect(url_for('home'))

    return redirect(url_for('index'))


# Simple Signup form backend
@app.route('/signup', methods=['GET', 'POST'])
def register():
    error = None

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
        if len(usernameInput) >= 4 and passwordInput == repeatpasswordInput and dbU.doesUsernameAlreadyExist(
                connection, usernameInput) and dbU.doesInvitationExist(connection, invitationInput) and len(
            passwordInput) >= 8 and not any(not c.isalnum() for c in usernameInput):
            error = "Dein Account wurde erstellt, logge dich nun ein"

            passwordInput = hashlib.md5(passwordInput.encode()).hexdigest()

            dbU.insertValueIntoUser(connection, usernameInput, passwordInput)

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


# Controlpanel
@app.route('/controlpanel', methods=['GET', 'POST'])
def controlpanel():
    error = None

    if not g.user:
        return redirect(url_for('index'))

    return render_template("controlpanel.html", error=error)


# "Main function" start of the Flask APP
if __name__ == '__main__':
    print('by Julian')

    print(initialize.get_request("network/connectionssummary"))

    app.run()
