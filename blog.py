from app import db, mail
from app.models import User, Post, Message, Notification, Task
from app import create_app       #application factory

app_instance = create_app()

#when using python shell we need to import db, User, Post from app towork on database
#now if flask shell is used those will be preimported ...
@app_instance.shell_context_processor
def make_shell_context():
	return {"db": db, "User": User, "Post": Post, "mail":mail, "Notification":Notification, "Message": Message, "Task":Task}

