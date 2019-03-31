from flask_mail import Message
from app import mail
from app import app_instance
from threading import Thread

def send_async_mail(app_instance, msg):
	with app_instance.app_context():
		mail.send(msg)


def send_mail(subject, sender, reciever, text, html):
	msg = Message(subject, sender=sender, recipients=reciever)
	msg.body = text
	msg.html = html
	#mail.send(msg)
	Thread(target = send_async_mail, args= (app_instance, msg)).start()


def send_password_request(user):

	#find token here if implemented in user model
	#not implemented
	send_mail(subject = "Password reset",
				sender = app_instance.config["ADMINS"][0],
				reciever= [user.mail],
				text = "Fake link generated",
				html = None)


















