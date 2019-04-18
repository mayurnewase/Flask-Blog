from app.main import main_bp as bp
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.main.forms import  EditProfile, PostForm, MesssageForm
from flask_login import current_user, login_user, logout_user, login_required  #manage sessions for user
from app.models import User, Post, Message, Notification
from app import db
from datetime import datetime

@bp.route("/")
@bp.route("/index", methods = ["GET", "POST"])
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
		return redirect(url_for("main.index"))     	#why redirect here, why not stay here only as index is already rendered? 
												#-> because for form submission POST request always send a web page response so if user refresh browser doesn't send same POST request to submit form.
	#read all posts from db
	
	posts = current_user.getAllPosts()

	return render_template("index.html", title = "Home", posts = posts, form=form)

@bp.route("/user/<name>")
@login_required
def user(name):
	user = User.query.filter_by(name= name).first_or_404()

	#dont get all posts get only posts for this user
	posts = user.posts.order_by(Post.timestamp.desc()) #possible coz of db.relationship of User and Post
	print("giving user template ", name)
	return render_template("user.html", user = user, posts = posts)


@bp.before_request
def before_request():
	#flask call this for every client request and before serving that request.
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()	  #no need to db.session.add(u) coz current_user runs user_loader which put user in db session

@bp.route("/edit_profile", methods = ["POST", "GET"])
def edit_profile():

	form = EditProfile()

	if form.validate_on_submit():
		print("---USER SENT FORM WITH ", request.method)
		current_user.name = form.name.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash("changes commited in db")

		return redirect(url_for("main.user", name = current_user.name))

	#how to prefill data in form so user will see old data and modify it,using GET request
	#coz when server gives web page to user it use get request.
	if request.method == "GET":
		form.name.data = current_user.name
		form.about_me.data = current_user.about_me


	return render_template("edit_profile.html", form = form)


@bp.route("/user/<name>/popup", methods = ["POST", "GET"])
@login_required
def user_popup(name):
	print("----------popup route hit----------")
	user = User.query.filter_by(name = name).first_or_404()
	return render_template("user_popup.html", user = user)


@bp.route("/send_message/<reciever>", methods =["POST", "GET"])
@login_required
def send_message(reciever):

	#inputs reciever name
	#get its object to pass in message table

	reciever_obj = User.query.filter_by(name = reciever).first_or_404()
	form  = MesssageForm()

	if form.validate_on_submit():
		print("----message sent-----")

		msg = Message(author = current_user, reciever = reciever_obj, body = form.message.data)
		db.session.add(msg)
		current_user.addNotification(notification_name = "unread_message",data = current_user.getMessagesCount())
		print(f"messages for {current_user.name} {current_user.getMessagesCount()}")
		db.session.commit()
		print(f"messages for {reciever_obj.name} {reciever_obj.getMessagesCount()}")

		flash("message sent successfully")

		return redirect(url_for("main.user", name = reciever))

	return render_template("send_message.html", form = form)


@bp.route("/read_message", methods = ["POST", "GET"])
@login_required
def read_message():

	#when user click on message badge
	#change last message checked to current time

	current_user.last_message_read_time = datetime.utcnow()
	current_user.addNotification(notification_name = "unread_message", data = 0)
	db.session.commit()

	messages_recieved_by_user = current_user.messages_recieved.order_by(Message.timestamp.desc())

	return render_template("read_message.html", messages = messages_recieved_by_user)


@bp.route("/notification_polling", methods = ["POST", "GET"])
@login_required	
def notification_polling():
	#client's browser will hit this route periodically for requesting latest notifications
	#server will query db for user's notifications and return a json response
	#to send only latest notifications
	since_parameter = request.args.get("since", 0.0, type = float)  #get since from url that client use to hit this route.if not found in url use 0 by default

	#send notifications ordered in old to new
	new_notifications = current_user.notifications.filter(Notification.timestamp > since_parameter).order_by(Notification.timestamp.asc())

	noti = [{"notification_name" : noti.notification_name, "data" : noti.get_data(), "timestamp" : noti.timestamp} for noti in new_notifications]
	noti = jsonify(noti)

	print(f"--------------client polling route hit for {current_user.name}  {noti}-------------")

	return noti

























