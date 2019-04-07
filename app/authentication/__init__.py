from flask import Blueprint
auth_bp = Blueprint("auth", __name__)
#auth -> blueprint name -> used to hit view functions from other bluprints 
#like auth.login, auth.register
#also by view func of this bp to call other view function -> in routes url_for(auth.index)
#but render_template take html file so it path to template from app/template/... -> like render_template(authentication/login.html)
#to call app's view functions call directly -> like url_for("index")
#to call other blueprint's view functions call by name -> like url_for(main.index)

from app.authentication import routes









