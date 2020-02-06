from flask import Flask, render_template, request , redirect , url_for
import sqlite3
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, Email
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\FFlaskApplication\\app\\database.db'
Bootstrap(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(15))
    
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=15)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'),Length(max=50)])
    username = StringField('username', validators=[InputRequired(),Length(min=5, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=15)])

@app.route('/')
def index():
    return render_template('index.html', result='')


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        query = (request.form['input_query'],)
        con = sqlite3.connect('diacompanion.db')
        cur = con.cursor()
        cur.execute("""SELECT name 
                       FROM constant_food 
                       WHERE category = ?""", (query))
        result = cur.fetchall()
        return render_template('index.html', result=result)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if user.password == form.password.data:
                return redirect(url_for('index'))
        return '<h1>Invalid username or password</h1>'    

    return render_template('login.html',form=form)


@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username = form.username.data, email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created</h1>'

    return render_template('signup.html',form=form)


if __name__ == '__main__':
    app.run(debug=True)
