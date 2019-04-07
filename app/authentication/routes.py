from app import app_instance as api
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, EditProfile, ResetPassword, PostForm
from flask_login import current_user, login_user, logout_user, login_required  #manage sessions for user
from app.models import User, Post
from app import db
from datetime import datetime
from app.authentication.email import send_password_request
from app.authentication import auth_bp as bp

@bp.route("/login", methods = ["POST", "GET"])
def login():

	if current_user.is_authenticated:				#current user from flask-login, if it is authenticated not then its anonymous.
		flash("user already logged in")
		return redirect(url_for("index"))

	form = LoginForm()
	if form.validate_on_submit():		#fails if user do get request to login page like without clicking submit / or any validation on field fails
		
		user = User.query.filter_by(name = form.name.data).first()		#first return uer obj only when entry is present
		if user is None or not user.check_password(form.password.data):
			flash("login failed")
			return redirect(url_for("auth.login"))

		login_user(user, remember = form.remember.data) 	#flask login function -> taking user object from db -> saves it in its session
															#now current_user variable will point to this user -> and its authenticated
		print("--------CURRENT USER-- ", current_user)
		flash("user logged in")
		return redirect(url_for("index"))

	return render_template("authentication/login.html", title = "sign in form", form = form)		#login failed -> try again

@bp.route("/logout", methods = ["POST", "GET"])
def logout():
	if current_user.is_authenticated:
		flash("logged out")
		logout_user()
		return redirect(url_for("auth.login"))


@bp.route("/register", methods = ["POST", "GET"])
def register():
	#add in db and redirect to index
	if current_user.is_authenticated:
		return redirect(url_for("index"))

	form = RegisterForm()
	if form.validate_on_submit():
		user = User(name=form.name.data, mail=form.mail.data)
		user.set_password(form.password1.data)

		db.session.add(user)
		db.session.commit()

		flash("registered {} with {} now can login".format(form.name.data, form.password1.data))

		return redirect(url_for("auth.login"))

	return render_template("authentication/register.html", form = form)

@bp.route("/reset_password", methods = ["POST", "GET"])
def reset_password():

	if current_user.is_authenticated:
		return redirect(url_for("index"))

	form = ResetPassword()

	if form.validate_on_submit():
		user = User.query.filter_by(mail = form.mail.data).first()

		if user:
			send_password_request(user)
			flash("Request sent check your mail")
			return redirect(url_for("auth.login"))
		else:
			flash("User not found")
			return redirect(url_for("auth.login"))

	return render_template("authentication/reset_password.html", form = form)













