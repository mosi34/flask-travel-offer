from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Email, Length, InputRequired
import scrape


app = Flask(__name__)
app.config['SECRET_KEY'] = 'somerandomkey'
Bootstrap(app)


class LoginForm (FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[
                           InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


@app.route('/')
def index():
    return render_template('main-page.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    city = request.form.get('whereYouAre')
    persons = request.form.get('persons')
    budget = request.form.get('price')
    ret = scrape.filter_b(budget=budget, peopleCount=persons)
    return render_template('results.html', data=ret)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(admin)
    return render_template('login.html')


@app.route('/<pageName>/')
def userpage(pageName):
    return render_template('userpage.html', username=pageName)


@app.route('/<pageName>/dashboard')
def admin(pageName):
    return render_template('dashboard.html', username=userpage)


if __name__ == '__main__':
    app.run(debug=True)
