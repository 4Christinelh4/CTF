from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, PasswordField, BooleanField,
                     EmailField)
from wtforms import validators
from wtforms.validators import InputRequired, Length

class Login(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

# username, password, email
class Register(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    create_username = StringField('Username', validators=[InputRequired()])
    create_password = PasswordField('Password', validators=[InputRequired()])

# form to make comment on a single course
# class Comment(FlaskForm):
#     comment = StringField("Comment", validators=[InputRequired()])