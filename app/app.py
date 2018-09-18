from functools import wraps
from flask import (Flask, flash, redirect, render_template, request,
                   session, url_for)
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from wtforms import Form, PasswordField, StringField, TextAreaField, validators

app = Flask(__name__)

# Config mysql
app.config['MYSQL_HOST'] = 'ec2-54-225-241-25.compute-1.amazonaws.com'
app.config['MYSQL_USER'] = 'oqrnhavmylzeql'
app.config['MYSQL_PASSWORD'] = '290ca06f7d3667c7ebeb2d89f1ed502ce9db4ff7d91d2fd4269e92f7052a2283'
app.config['MYSQL_DB'] = 'd49pt4ur37g33c'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MYSQL
mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    cur.close()

    return render_template('index.html', articles=articles)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    cur.close()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No article found, please add article to view them here'
        return render_template('articles.html', msg=msg)


@app.route('/article/<string:id>/', methods=['GET'])
def article(id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM articles WHERE id ={}".format(id))

    article = cur.fetchone()

    cur.close()

    return render_template('article.html', article=article)


class RegisterForm(Form):
    name = StringField(u'Name', validators=[validators.input_required()])
    username = StringField(u'Username', validators=[validators.optional()])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
            (name,
             email,
             username,
             password))

        # Commit to DB
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))

    return render_template('register.html', form=form)


# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # GEt form values
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute(
            "SELECT * FROM users WHERE username = %s",
            [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            cur.close()
            if sha256_crypt.verify(password_candidate, password):
                # Password and username matches
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))

            else:
                error = 'Password or username incorrect, Invalid login'
                return render_template('login.html', error=error)
            # close connection
        else:
            error = "Username not found"
            return render_template('login.html', error=error)

    return render_template('login.html')


# Check for user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorised, Please log in to continue to this page', 'danger')
            return redirect(url_for('login'))
    return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You have successfully logged out', 'success')
    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    cur.close()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No article found, please add article to view them here'
        return render_template('dashboard.html', msg=msg)


class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])


# Add article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create cursor
        cursor = mysql.connection.cursor()

        cursor.execute(
            "INSERT INTO articles(title, author, body) VALUES(%s, %s, %s);",
            (title,
             session['username'],
             body))

        # Commit to DB
        mysql.connection.commit()

        # close connection
        cursor.close()

        flash('Article Created successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM articles WHERE id = {}".format(id))

    article = cur.fetchone()

    form = ArticleForm(request.form)

    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create cursor
        cursor = mysql.connection.cursor()

        cursor.execute(
            "UPDATE articles SET title={}, body={} WHERE id={}".format(
                title, body, id))

        # Commit to DB
        mysql.connection.commit()

        # close connection
        cursor.close()

        flash('Article Updated successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


@app.route('/delete_article', methods=['POST'])
@is_logged_in
def delete_article(id):
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM articles WHERE id = {}".format(id))

    mysql.connection.commit()

    cur.close()


if __name__ == '__main__':
    app.secret_key = 'secret_key_219641456885_krafty'
    app.run(debug=False)
