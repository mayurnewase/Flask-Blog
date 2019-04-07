from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User

class EditProfile(FlaskForm):
	name = StringField("Name", validators = [DataRequired()])
	about_me = StringField("About Me", validators = [Length(min=0, max=140)])
	submit = SubmitField("Push it")

class PostForm(FlaskForm):
	post = TextAreaField("Your Opinion..", validators=[DataRequired(), Length(min=1, max=140)])
	submit = SubmitField("Post it")












