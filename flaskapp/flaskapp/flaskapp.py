from flask import Flask, render_template, request, g, redirect, url_for, session
from collections import Counter
import sqlite3

app = Flask(__name__, template_folder='templates')

app.secret_key = 'super secret key'

DATABASE = '/var/www/html/flaskapp/database.db'

app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        query = 'SELECT * FROM users WHERE username = ? AND password = ?'
        args = (username, password,)
        account = execute_query(query, args)
        if len(account) > 0 and account[0]:
            print account
            session['loggedin'] = True
            session['id'] = account[0][0]
            session['username'] = account[0][1]
            session['firstname'] = account[0][3]
            session['lastname'] = account[0][4]
            session['email'] = account[0][5]
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('firstname', None)
    session.pop('lastname', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        query = 'SELECT * FROM users WHERE username = ?'
        args = (username, )
        account = execute_query(query, args)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
             query = 'INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?)'
             args = (username, password, firstname, lastname, email, )
             execute_query(query, args)
             msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('registration.html', msg = msg)

@app.route('/countme/<input_str>')
def count_me(input_str):
    input_counter = Counter(input_str)
    response = []
    for letter, count in input_counter.most_common():
        response.append('"{}": {}'.format(letter, count))
    return '<br>'.join(response)

@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM users""") + execute_query("""SELECT * FROM uploads""")
    return '<br>'.join(str(row) for row in rows)

if __name__ == '__main__':
  app.run()
