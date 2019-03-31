from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User

class LoginForm(FlaskForm):
	name = StringField("name", validators = [DataRequired()])
	password = PasswordField("password", validators = [DataRequired()])
	remember = BooleanField("Remember me lmao")

	submit = SubmitField("Let me in")




class RegisterForm(FlaskForm):
	name = StringField("name", validators = [DataRequired()])
	mail = StringField("mail", validators = [DataRequired(), Email()])
	password1 = PasswordField("password1", validators = [DataRequired()])
	password2 = PasswordField("password2", validators = [DataRequired(), EqualTo("password1")])

	submit = SubmitField("Let me in")



	def validate_name(self, name):
		#this is also callback function
		#any function start with validate_<any> -> wtform make it validator for <any> -> jeesus christ

		res = User.query.filter_by(name = name.data).first()
		if res is not None:
			raise ValidationError("Taken")

	def validate_mail(self, mail):
		res = User.query.filter_by(mail = mail.data).first()
		if res is not None:
			raise ValidationError("Taken")


class EditProfile(FlaskForm):
	name = StringField("Name", validators = [DataRequired()])
	about_me = StringField("About Me", validators = [Length(min=0, max=140)])
	submit = SubmitField("Push it")



class ResetPassword(FlaskForm):
	mail = StringField("mail", validators = [DataRequired(), Email()])
	submit = SubmitField("Reset it")

class PostForm(FlaskForm):
	post = TextAreaField("Your Opinion..", validators=[DataRequired(), Length(min=1, max=140)])
	submit = SubmitField("Post it")












