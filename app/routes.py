from app import app_instance as api
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required  #manage sessions for user
from app.models import User
from app import db

@api.route("/")
@api.route("/index")
@login_required              #protect this function -> also adds ?next parameter in url to remember where to go next after logged in
def index():					#need to inspect next parameter in login(), as hacker can put protected page address in next and it will redirect there.
	
	#user = {"name" : "lola"}  #not required as index.html take it from db

	posts = [
	{"author" : {"name" : "lola_author"}, "body" : "lola wrote a book"},
	{"author" : {"name" : "lola_second_author"}, "body" : "aother book"}
	]

	return render_template("index.html", title = "Home", posts = posts)


@api.route("/login", methods = ["POST", "GET"])
def login():

	if current_user.is_authenticated:				#current user from flask-login, if it is authenticated not then its anonymous.
		flash("user already logged in")
		return redirect(url_for("index"))

	form = LoginForm()
	if form.validate_on_submit():		#fails if user do get request to login page like without clicking submit / or any validation on field fails
		
		user = User.query.filter_by(name = form.name.data).first()		#first return uer obj only when entry is present
		if user is None or not user.check_password(form.password.data):
			flash("login failed")
			return redirect(url_for("login"))

		login_user(user, remember = form.remember.data) 	#flask login function -> taking user object from db -> saves it in its session
															#now current_user variable will point to this user -> and its authenticated
		print("--------CURRENT USER-- ", current_user)
		flash("user logged in")
		return redirect(url_for("index"))

	return render_template("/login.html", title = "sign in form", form = form)		#login failed -> try again

@api.route("/logout", methods = ["POST", "GET"])
def logout():
	if current_user.is_authenticated:
		flash("logged out")
		logout_user()
		return redirect(url_for("login"))


@api.route("/register", methods = ["POST", "GET"])
def register():
	#add in db and redirect to index
	if current_user.is_authenticated:
		return redirect(url_for("index"))

	form = RegisterForm()
	print("------INSIDE FORM VIEW FUNCTION-----------")
	if form.validate_on_submit():
		print("----INSIDE VALIDATED FORM------")
		user = User(name=form.name.data, mail=form.mail.data)
		user.set_password(form.password1.data)

		db.session.add(user)
		db.session.commit()

		flash("registered {} with {} now can login".format(form.name.data, form.password1.data))

		return redirect(url_for("login"))

	return render_template("/register.html", form = form)















