    
from flask import render_template, request
from app.errors import errors_bp as bp
from app import db
from app.api.errors import error_response as api_error_response

def wants_json_response():
	return request.accept_mimetypes["application/json"] >= request.accept_mimetypes["text/html"]

@bp.app_errorhandler(404)
def not_found_error(error):
	print("-----URL NOT FOUND-----")

	if wants_json_response():
		print("-----returning json error")
		return api_error_response(404)

	print("--------returning html error")
	return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):	#Not able to catch this error
	print("===================INTERNAL ERROR CATCHED====================")
	db.session.rollback()

	if wants_json_response():
		print("-----returning json error")
		return api_error_response(500)

	print("-----returning html error")
	return render_template('errors/500.html'), 500




