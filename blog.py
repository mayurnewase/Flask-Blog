from app import app_instance, db, mail
from app.models import User, Post


#when using python shell we need to import db, User, Post from app towork on database
#now if flask shell is used those will be preimported ...
@app_instance.shell_context_processor
def make_shell_context():
	return {"db": db, "User": User, "Post": Post, "mail":mail}

