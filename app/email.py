from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail

def send_async_mail(app_instance, msg):
	with app_instance.app_context():
		mail.send(msg)


def send_mail(subject, sender, reciever, text, html, attatchments = None, sync = False):
	msg = Message(subject, sender=sender, recipients=reciever)
	msg.body = text
	msg.html = html
	
	if attatchments:
		#attachment will contain  filename, media type, file data -> used to export posts
		for att in attachments:
			msg.attach(*att)   #att wil be tuple of above values -> * will expand it in 3 parameters
	
	if sync:
		#send in foreground
		#used by background task
		mail.send(msg)

	else:
		#send in other thread
		#used by main app to send password forget link

		Thread(target = send_async_mail, args=(current_app._get_current_object(), msg)).start()  #cant use app_instance directly -> so get it by current_app
		"""
			current_app is a context-aware variable that is tied to the thread.
			that is handling the client request. In a different thread,
			current_app would not have a value assigned.
		"""






