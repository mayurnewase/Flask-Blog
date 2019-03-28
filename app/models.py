#database structure

from app import db #from init.py -> instance of sql daydabase
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), index = True, unique = True)
	mail = db.Column(db.String(120), index = True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship("Post", backref = "author", lazy="dynamic")  #Post is following table -> this is not field in user table -> just a link

	#he backref argument defines the name of a field that will be added to the objects of the "many" class that points back at the "one" object.

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	user_id = db.Column(db.Integer, db.ForeignKey("user.id")) #user is db table name of above class -> incosistancy













