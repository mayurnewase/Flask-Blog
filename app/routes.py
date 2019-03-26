from app import app_instance as api

@api.route("/")
@api.route("/index")
def index():
	return "hello"








