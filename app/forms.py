from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtfforms.validaotrs import Length, EqualTo, Email, DataRequired, ValidationError

class RegisterForm(FlaskForm):
    username = StringField('User Name', validators = [Length(min =2,max = 30), DataRequired()])
    email = StringField('Email Address', validators = [Email(), DataRequired()])
    password1 = PasswordField('Password', validators = [Length(min = 5)], DataRequired())
    password2 = PasswordField('Confirm Password', validators = [EqualTo('password1'), DataRequired()]) 
    submit = SubmitField('Create Account')