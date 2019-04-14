from flask import Flask, render_template, redirect, url_for, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
    return render_template('home-multipage.html')

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return "Awesome"
    return render_template('signin.html', error=error)

if __name__ == "__main__":
    app.run()