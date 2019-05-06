from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES   #code -> text

def error_response(status_code, message = None):
	#take error code and message
	#return json of text error and message

	payload = {"error" : HTTP_STATUS_CODES.get(status_code, "unknown error")}

	if message:
		payload["message"] = message

	response = jsonify(payload)
	return response

def bad_request(message):
    return error_response(400, message)










