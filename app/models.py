#database structure

from app import db #from init.py -> instance of sql daydabase
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login #from init.py -> instance of flask login

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), index = True, unique = True)
	mail = db.Column(db.String(120), index = True)
	password_hash = db.Column(db.String(128))
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default = datetime.utcnow)

	#he backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object.
	posts = db.relationship("Post", backref = "author", lazy="dynamic")  #Post is following table -> this is not field in user table -> just a link

	def set_password(self, password):
		#helper for hashing
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		#helper for hashing
		return check_password_hash(self.password_hash, password)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	user_id = db.Column(db.Integer, db.ForeignKey("user.id")) #user is db table name of above class -> incosistancy


@login.user_loader  #for flask-login
def load_user(id):
	#for flask login save user id in flask user session,but it doesn't know db.So app has to give it user from db.
	#WHO IS PASSING THE ID ?? -> IS IT current_user.
	return User.query.get(int(id))









