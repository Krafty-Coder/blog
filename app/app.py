from functools import wraps
from flask import (Flask, flash, redirect, render_template, request,
                   session, url_for)
from app.models import cur, conn
from passlib.hash import sha256_crypt
from wtforms import Form, PasswordField, StringField, TextAreaField, validators

app = Flask(__name__)

def create_cur():
    return conn.cursor()

@app.route('/')
def index():
    create_cur()
    cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    cur.close()

    return render_template('index.html', articles=articles)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    create_cur()
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()


    if result:
        cur.close()
        return render_template('articles.html', articles=articles)
    else:
        cur.close()
        msg = 'No article found, please add article to view them here'
        return render_template('articles.html', msg=msg)


@app.route('/article/<string:id>/', methods=['GET'])
def article(id):
    create_cur()
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
    create_cur()
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur.execute(
            "INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
            (name,
             email,
             username,
             password))

        # Commit to DB
        conn.commit()
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))

    return render_template('register.html', form=form)


# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    create_cur()
    if request.method == 'POST':
        # GEt form values
        username = request.form['username']
        password_candidate = request.form['password']

        # Get user by username
        result = cur.execute(
            "SELECT * FROM users WHERE username = %s",
            [username])

        if result:
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
            cur.close()
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
    create_cur()
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    cur.close()

    if result:
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
    create_cur()
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create cursor
        cur.execute(
            "INSERT INTO articles(title, author, body) VALUES(%s, %s, %s);",
            (title,
             session['username'],
             body))

        # Commit to DB
        conn.commit()

        # close connection
        cur.close()

        flash('Article Created successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    create_cur()
    cur.execute("SELECT * FROM articles WHERE id = {}".format(id))

    article = cur.fetchone()

    form = ArticleForm(request.form)

    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        cur.execute(
            "UPDATE articles SET title={}, body={} WHERE id={}".format(
                title, body, id))

        # Commit to DB
        conn.commit()

        # close connection
        cur.close()

        flash('Article Updated successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


@app.route('/delete_article', methods=['POST'])
@is_logged_in
def delete_article(id):
    create_cur()
    cur.execute("DELETE FROM articles WHERE id = {}".format(id))

    conn.commit()

    cur.close()


if __name__ == '__main__':
    app.secret_key = 'secret_key_219641456885_krafty'
    app.run(debug=False)
