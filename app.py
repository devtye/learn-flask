from flask import Flask , render_template, redirect, url_for, request, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

#manual db import
#import sqlite3

app = Flask(__name__)

app.secret_key = "devill may cry"

#app.database = "sample.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

#adds significant overhead and will be disabled by default in the future.  Set it to True to suppress this warning.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


from models import *


#SQLAlchemy OBJ
db = SQLAlchemy(app)

#password fucntion
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in'in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

#index-  the landing route
@app.route('/')
@login_required
def home():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", posts=posts)


#other page route
@app.route('/smartsheet_demo')
def smartsheet_demo():
    return render_template("smartsheet_demo.html")


#app page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    error= None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


#logout page route
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out.')
    return redirect(url_for('home'))


#database connetion route
def connect_db():
    return sqlite3.connect('posts.db')

if __name__ ==  '__main__':
    app.run(debug=True)




