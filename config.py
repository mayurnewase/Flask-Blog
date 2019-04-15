import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__)) #c:/.../Microblog/
load_dotenv(os.path.join(basedir, ".env"))		#../microblog/.env
#this sets enviroment with variables from .env file
# so secret stays on computer as this file is shared

class Config(object):
	SECRET_KEY = os.environ.get("SECRET_KEY") or "lmao-this-is-secret"   #variable name should be same

	SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///"+os.path.join(basedir,"app.db")
	#SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") #for heroku use cuz its not using postgress -> and losing data on restart
	
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER=os.environ.get("MAIL_SERVER")
	MAIL_PORT=os.environ.get("MAIL_PORT")
	MAIL_USE_TLS = None
	ADMINS = ['admin@gmail.com']

	#MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	#MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

	LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")    #Not used currentlt as I did not create support for logging



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


















