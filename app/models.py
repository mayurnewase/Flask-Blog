#database structure

from app import db #from init.py -> instance of sql daydabase
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login #from init.py -> instance of flask login
import time
import json

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), index = True, unique = True)
	mail = db.Column(db.String(120), index = True)
	password_hash = db.Column(db.String(128))
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default = datetime.utcnow)

	last_message_read_time = db.Column(db.DateTime)      #Save when user read message last time.used to find how many unseen messages are remaining.
	#he backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object.
	posts = db.relationship("Post", backref = "author", lazy="dynamic")  #Post is following table -> this is not field in user table -> just a link

	#WHAT IS FOREIGN KEY HERE ?
	#here backref should be sender but author used so same _post subtemplate logic can be used
	#so now to add message in db -> msg = Message(author, reciever)  #pass objects of both
	#then db.session.add(msg)

	#to read messages for user from db -> user_object.messages_recieved
	messages_sent = db.relationship("Message", foreign_keys = "Message.sender_id", backref = "author", lazy = "dynamic")
	messages_recieved = db.relationship("Message", foreign_keys = "Message.reciever_id", backref = "reciever", lazy = "dynamic")

	#to read notifications for user from db -> user_object.notifications
	notifications = db.relationship("Notification", backref = "user", lazy = "dynamic")

	def set_password(self, password):
		#helper for hashing
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		#helper for hashing
		return check_password_hash(self.password_hash, password)

	def getAllPosts(self):
		#can be used to get specific posts but for now return all posts from db
		posts = Post.query.all()
		return posts

	def getMessagesCount(self):
		#Function to find unseen messages count for current user thats why self
		#this will be called in read_message template by jinja to display counter
		#uses current user object to find messages for current user
		#then filters them by last_message_seen time
		last_read_time = self.last_message_read_time or datetime(1900, 1, 1)  #set to oldest so all messges are marked as unseen
		return Message.query.filter_by(reciever = self).filter(Message.timestamp > last_read_time).count()

	def addNotification(self, notification_name, data):
		#this will add notification for user in db
		#if anyone send message he will also add it in db
		#in any place where badge count change it should also add notification -> 2 places -> send_message() and read_messages()

		#if exists remove it
		#WHY ITS USED LIKE notificaitons.filter_by() WHY NOT Notificaitons.query.filter_by()
		self.notifications.filter_by(notification_name = notification_name).delete()
		n = Notification(notification_name = notification_name, json_payload = json.dumps(data), user = self)
		db.session.add(n)
		#db.session.commit()
		return n


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id")) #user is db table name of above class -> incosistancy

class Message(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	sender_id = db.Column(db.Integer, db.ForeignKey(User.id))
	reciever_id = db.Column(db.Integer, db.ForeignKey(User.id))
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)

class Notification(db.Model):
	#model for keeping track of all user notifications for new messages.
	id = db.Column(db.Integer, primary_key = True)
	notification_name = db.Column(db.String(128), index = True)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"))   #foreign key to user id
	timestamp = db.Column(db.Float, index = True, default = time.time)   #get default value from time.time() why not datetime.utcnow()
																		#-> because user give time in "since" parameter.its single valued float
	json_payload = db.Column(db.Text)

	def get_data(self):
		#for json deserialization
		return json.loads(str(self.json_payload))


@login.user_loader  #for flask-login
def load_user(id):
	#for flask login save user id in flask user session,but it doesn't know db.So app has to give it user from db.
	#WHO IS PASSING THE ID ?? -> IS IT current_user.
	return User.query.get(int(id))









