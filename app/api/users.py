from app.api import api_bp
from app.models import User
from flask import jsonify, request, url_for
from app.api.errors import bad_request
from app import db

@api_bp.route("/users/<int:id>", methods = ["GET"])
def get_user(id):
	#take id and return user object jsonified

	obj = User.query.get_or_404(id)   #if is not found this raise 404 error which is handled by
										#old error handling module -> it should be handled by error.py to send error in json format
										#for that use mimetypes -> client specify if he want html error or json error
	user_dict = obj.to_dict()			
	json_obj =  jsonify(user_dict)
	return json_obj

@api_bp.route("/users", methods = ["GET"])
def get_users():
	#get collection of all users -> not used as pagination logic is not used
	#see in miguel blog
	pass

@api_bp.route("/users", methods = ["POST"])
def create_user():
	#this request should be post
	#means request should have data inside it
	#unlike get data is in url

	#test this with httpie module from terminal
	#eg -> http POST http://127.0.0.1:5000/api/users name="madhuri" password="nene"

	data = request.get_json() or {}

	if "name" not in data or "mail" not in data or "password" not in data:
		return bad_request("must include name mail and password")

	if User.query.filter_by(name = data["name"]).first():
		return bad_request("name already exixts")

	user = User()
	print("---data got ", data)
	user.from_dict(data, new_user = True)
	db.session.add(user)
	db.session.commit()

	response = jsonify(user.to_dict())
	response.status_code = 201

	#this is required by http protocol that 201 code should have link to new resource
	response.headers["location"] = url_for("api.get_user", id = user.id) #why is this used ?

	return response
	

@api_bp.route("/users/<int:id>", methods = ["PUT"])
def update_user(id):
	
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'name' in data and data['name'] != user.username and \
            User.query.filter_by(name=data['name']).first():
        return bad_request('please use a different username')
    if 'mail' in data and data['mail'] != user.mail and \
            User.query.filter_by(mail=data['mail']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    
    return jsonify(user.to_dict())































