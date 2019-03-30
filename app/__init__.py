from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app_instance = Flask(__name__)
app_instance.config.from_object(Config)
db = SQLAlchemy(app_instance)
migrate = Migrate(app_instance, db)

#login need 4 mandatory functions in user model
#is_authenticated, is_active, is_anonymous, get_id
#but UserMixin can be used so no need to use above functions
login = LoginManager(app_instance)
login.login_view = "login" #to force user go to "/login" if not already logged in. -> Use @loggin_required to protect index function.

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


