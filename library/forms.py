from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class Registration_Form(FlaskForm):
    user_name = StringField('User name', validators=[DataRequired('Must not be empty')])
    user_password = PasswordField('New password', validators=[
        DataRequired('Must not be empty'),
        EqualTo('repeat_password', message='Password must much') 
    ])
    repeat_password = PasswordField('Repeat password', validators=[DataRequired('Must not be empty')])
    submit = SubmitField('Register')

class Login_Form(FlaskForm):
    user_name = StringField('User name', validators=[DataRequired('Must not be empty')])
    user_password = PasswordField('User password', validators=[DataRequired('Enter your password')])
    login = SubmitField('Login')