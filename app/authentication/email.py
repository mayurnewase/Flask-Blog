from flask_mail import Message
from app import mail
#from app import app_instance #removed for applicaiton factory
from threading import Thread
from flask import current_app

def send_async_mail(app_instance, msg):
	with app_instance.app_context():
		mail.send(msg)


def send_mail(subject, sender, reciever, text, html):
	msg = Message(subject, sender=sender, recipients=reciever)
	msg.body = text
	msg.html = html
	#mail.send(msg)
	Thread(target = send_async_mail, args=(current_app._get_current_object(), msg)).start()  #cant use app_instance directly -> so get it by current_app
	"""
	current_app is a context-aware variable that is tied to the thread.
	that is handling the client request. In a different thread,
	current_app would not have a value assigned.
	"""

def send_password_request(user):

	#find token here if implemented in user model
	#not implemented
	send_mail(subject = "Password reset",
				sender = current_app.config["ADMINS"][0],
				reciever= [user.mail],
				text = "Fake link generated",
				html = None)


















