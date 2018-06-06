from flask import Flask, render_template, url_for, redirect, request


app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

@app.route('/cards')
def cards():
    return render_template('cards.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/forgotp')
def forgotp():
    return render_template('forgot-password.html')

@app.route('/blank')
def blank():
    return render_template('blank.html')

if __name__ == "__main__":
    app.debug = True
    app.run()