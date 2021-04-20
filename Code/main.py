from flask import Flask, render_template, redirect, url_for, request, make_response, g, session, Response

# Initialize the Flask APP
app = Flask(__name__)

# Secret App key for Session usage
app.secret_key = "sLWqVgyq8ZEQMK0AdaQrBcHlw36fo6K23f83zxbwsiYetQQzbbeqJdAXg3JJz5Mz2vepPS8lM6g2CLapqpPbMv56K5R3PROJ2iXa9XzwiqunRxRsSIppmqZ0Q6JMg"


# Default Index route site
@app.route('/')
def index():
    return render_template('index.html')


# Default explanations site
@app.route('/was-ist-das')
def help():
    return render_template('help.html')


# Error handler sites
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.route('/login', methods=['GET', 'POST'])
def welcome():
    print("Still work to do")
    # TODO


# "Main function" start of the Flask APP
if __name__ == '__main__':
    print('by Julian')

    app.run()
