from app.email import send_mail

def send_password_request(user):

	#find token here if implemented in user model
	#not implemented
	send_mail(subject = "Password reset",
				sender = current_app.config["ADMINS"][0],
				reciever= [user.mail],
				text = "Fake link generated",
				html = None)















