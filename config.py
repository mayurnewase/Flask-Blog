import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get("SECRET_KEY") or "lmao-this-is-secret"   #varaible name should be same

	SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///"+os.path.join(basedir,"app.db")
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER="localhost"
	MAIL_PORT=8025
	#MAIL_SERVER = os.environ.get('MAIL_SERVER')
	#MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['admin@gmail.com']

	"""
	to start local server
	python -m smtpd -n -c DebuggingServer localhost:8025

	for google
	(venv) $ export MAIL_SERVER=smtp.googlemail.com
	(venv) $ export MAIL_PORT=587
	(venv) $ export MAIL_USE_TLS=1
	(venv) $ export MAIL_USERNAME=<your-gmail-username>
	(venv) $ export MAIL_PASSWORD=<your-gmail-password>
	"""


















