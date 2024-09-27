from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

def check_email(form, field):
    email = field.data
    if "utoronto.ca" not in email:
        raise ValidationError("Email must be a UofT email address")

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired("Please add your first and last name.")])
    email = StringField('What is your UofT Email address?', validators=[DataRequired("Please enter a valid email address"), Email(message = "Please include an @ in the email address."), check_email])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        
        if old_name is not None and old_name != form.name.data:
            flash('Looks like your name is changed!')
        
        if old_email is not None and old_email != form.email.data:
            flash('Looks like your email is changed!')
        
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

