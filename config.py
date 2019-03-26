import os


class Config(object):
	SECRET_KEY = os.environ.get("SECRET_KEY") or "lmao-this-is-secret"   #varaible name should be same



	