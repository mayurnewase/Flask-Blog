from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	name = StringField("name", validators = [DataRequired()])
	password = PasswordField("password", validators = [DataRequired()])
	remember = BooleanField("Remember me lmao")

	submit = SubmitField("Let me in")






