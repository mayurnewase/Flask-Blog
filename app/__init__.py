from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap

from redis import Redis
import rq

#initialize empty flask extensions and initialize after app is made
db = SQLAlchemy()  #take app_instance
migrate = Migrate() #take app_instance,db
mail = Mail()   #take app_instance
bootstrap = Bootstrap()  #now booststrap/base.html is available to use.so base.html can use it
									#take app_instance
#login need 4 mandatory functions in user model
#is_authenticated, is_active, is_anonymous, get_id
#but UserMixin can be used so no need to use above functions
login = LoginManager() #takes app_instance

def create_app(config_class = Config):
	#Application factory function now can take config class
	#Used to create app for various configurations(loke dev and testing configs)

	app_instance = Flask(__name__)
	app_instance.config.from_object(config_class)
	
	db.init_app(app_instance)
	migrate.init_app(app_instance, db)
	mail.init_app(app_instance)
	bootstrap.init_app(app_instance)
	login.init_app(app_instance)

	login.login_view = "auth.login" #to force user go to "/login" if not already logged in. -> Use @loggin_required to protect index function.

	#Blueprints

	from app.errors import errors_bp
	app_instance.register_blueprint(errors_bp)   #connects view function, templates, static files, error handlers to flask app

	from app.authentication import auth_bp
	app_instance.register_blueprint(auth_bp, url_prefix = "/auth") 
	#prefix for seperating view functions
	#http://127.0.0.1:5000/login   =>  http://127.0.0.1:5000/auth/login
	#optional
	#we are using url_for() to call view functions of this blueprint (like auth.login),prefix is appended automatically

	from app.main import main_bp
	app_instance.register_blueprint(main_bp, url_prefix = "/main")

	#bind redis queue to app so we can access current_app.task_queue
	app_instance.redis = Redis.from_url(app_instance.config["REDIS_URL"])
	app_instance.task_queue = rq.Queue(app_instance.config["REDIS_QUEUE"], connection = app_instance.redis)

	return app_instance

"""
from jinja2 import Environment
jinja_env = Environment(extensions=['jinja2.ext.i18n'])
def debug(data):
	print(data)
	return ""
jinja_env.filters["debug"] = debug
"""

from app import models




"""
To add form
1.Form fields and validators in forms.py
2.form html template
3.view function to handle form data
4.link to hit that url
"""

"""
flask env vars
FLASK_ENV=developement
FLASK_APP=blog.py
FLASK_DEBUG=1
"""

"""
contexts variables and methods:
	applicaion context:
		current_app
		g
		to push it manually -> app_instance.app_context().push()
	request context:
		current_user
		request
		session

"""

"""
Organize with Blueprints
1.Error Handling blueprint
	
	app/
	    errors/                             <-- blueprint package
	        __init__.py                     <-- blueprint creation
	        handlers.py                     <-- error handlers
	    templates/
	        errors/                         <-- error templates
	            404.html
	            500.html
	    __init__.py                         <-- blueprint registration

2.Authentication blueprint

	app/
		auth/
			__init__py                 <--create bp
			email.py
			routes.py
			forms.py
		templates/
			auth/
				login.html
				register.html
				reset_password.html
		__init__.py                    <-- register bp

3.Main blueprint
	app/
		main/
			__init__.py        <-- create bp here
			forms.py
			routes.py
		templates/
			_post.html
			base.html
			edit_profile.html
			index.html
			user.html
	
	__init__.py      <-- register bp here

-------------------------------------------
adding background tasks with rq
	collect all posts
	send it to user via mail

	also add support to send mail in foreground for background task

	steps:
		restart redis -> sudo systemctl restart redis-server
		run redis worker -> rq worker microblog-tasks
		run app -> flask run
"""





