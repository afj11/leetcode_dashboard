from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Leetcode Username', validators=[DataRequired()])
    password = PasswordField('Leetcode password', validators=[DataRequired()])
    submit = SubmitField('Submit')
