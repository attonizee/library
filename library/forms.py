from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
    remember = BooleanField('Remember me', default=False)
    login = SubmitField('Login')

class Add_Book(FlaskForm):
    book_name = StringField('Book name', validators=[DataRequired('Must not be empty')])
    author_name = StringField('Author name', validators=[DataRequired('Must not be empty')])
    add_button = SubmitField('Add')