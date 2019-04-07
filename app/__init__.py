from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap


app_instance = Flask(__name__)
app_instance.config.from_object(Config)
db = SQLAlchemy(app_instance)
migrate = Migrate(app_instance, db)
mail = Mail(app_instance)
bootstrap = Bootstrap(app_instance)  #now booststrap/base.html is available to use.so base.html can use it

#login need 4 mandatory functions in user model
#is_authenticated, is_active, is_anonymous, get_id
#but UserMixin can be used so no need to use above functions
login = LoginManager(app_instance)
login.login_view = "login" #to force user go to "/login" if not already logged in. -> Use @loggin_required to protect index function.

#Blueprints

from app.errors import errors_bp
app_instance.register_blueprint(errors_bp)   #connects view function, templates, static files, error handlers to flask app

from app.authentication import auth_bp
app_instance.register_blueprint(auth_bp, url_prefix = "/auth") 
#prefix for seperating view functions
#http://127.0.0.1:5000/login   =>  http://127.0.0.1:5000/auth/login
#optional
#we are using url_for() to call view functions of this blueprint (like auth.login),prefix is appended automatically

from app import routes, models


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
"""





