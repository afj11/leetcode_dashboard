from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Leetcode Username', validators=[DataRequired()])
    companyname = StringField('Company Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
    show_more_companies = SubmitField('Show all')