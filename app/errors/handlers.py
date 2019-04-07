    
from flask import render_template
from app.errors import errors_bp as bp


@bp.app_errorhandler(404)
def not_found_error(error):
	print("-----URL NOT FOUND-----")
	return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):	#Not able to catch this error
	print("===================INTERNAL ERROR CATCHED====================")
	db.session.rollback()
	return render_template('errors/500.html'), 500




