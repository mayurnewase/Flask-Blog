    
from flask import render_template
from app import app_instance as api


@api.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404


@api.errorhandler(500)
def internal_error(error):	#Not able to catch this error
	print("===================INTERNAL ERROR CATCHED====================")
	db.session.rollback()
	return render_template('500.html'), 500