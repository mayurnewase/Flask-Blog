from app import app_instance as api
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, EditProfile, ResetPassword, PostForm
from flask_login import current_user, login_user, logout_user, login_required  #manage sessions for user
from app.models import User, Post
from app import db
from datetime import datetime

@api.route("/")
@api.route("/index", methods = ["GET", "POST"])
@login_required              #protect this function -> also adds ?next parameter in url to remember where to go next after logged in
def index():					#need to inspect next parameter in login(), as hacker can put protected page address in next and it will redirect there.
	
	#user = {"name" : "lola"}  #not required as index.html take it from db

	#form to accept post from user
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body= form.post.data, author = current_user)  #author is backref from user to post
		db.session.add(post)
		db.session.commit()
		print("=========post submitted===========")
		flash("Post submitted")
		return redirect(url_for("index"))     	#why redirect here, why not stay here only as index is already rendered? 
												#-> because for form submission POST request always send a web page response so if user refresh browser doesn't send same POST request to submit form.
	#read all posts from db
	
	posts = current_user.getAllPosts()

	return render_template("index.html", title = "Home", posts = posts, form=form)

@api.route("/user/<name>")
@login_required
def user(name):
	user = User.query.filter_by(name= name).first_or_404()

	#dont get all posts get only posts for this user
	posts = user.posts.order_by(Post.timestamp.desc()) #possible coz of db.relationship of User and Post
	print("giving user template ", name)
	return render_template("user.html", user = user, posts = posts)


@api.before_request
def before_request():
	#flask call this for every client request and before serving that request.
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()	  #no need to db.session.add(u) coz current_user runs user_loader which put user in db session

@api.route("/edit_profile", methods = ["POST", "GET"])
def edit_profile():

	form = EditProfile()

	if form.validate_on_submit():
		print("---USER SENT FORM WITH ", request.method)
		current_user.name = form.name.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash("changes commited in db")

		return redirect(url_for("user", name = current_user.name))

	#how to prefill data in form so user will see old data and modify it,using GET request
	#coz when server gives web page to user it use get request.
	if request.method == "GET":
		form.name.data = current_user.name
		form.about_me.data = current_user.about_me


	return render_template("edit_profile.html", form = form)











