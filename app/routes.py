from app import app_instance as api
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@api.route("/")
@api.route("/index")
def index():
	user = {"name" : "lola"}

	posts = [
	{"author" : {"name" : "lola_author"}, "body" : "lola wrote a book"},
	{"author" : {"name" : "lola_second_author"}, "body" : "aother book"}
	]

	return render_template("index.html", title = "Home", user = user, posts = posts)



@api.route("/login", methods = ["POST", "GET"])
def login():
	form = LoginForm()
	if form.validate_on_submit():		#fails if user do get request to login page like without clicking submit / or any validation on field fails
		flash("Login success by user {}, remember {}".format(form.name.data, form.remember.data))
		return redirect(url_for("index"))

	return render_template("/login.html", title = "sign in form", form = form)		#login failed -> try again





