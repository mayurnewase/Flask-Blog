from app import app_instance as api
from flask import render_template

@api.route("/")
@api.route("/index")
def index():
	user = {"name" : "lola"}

	posts = [
	{"author" : {"name" : "lola_author"}, "body" : "lola wrote a book"},
	{"author" : {"name" : "lola_second_author"}, "body" : "aother book"}
	]


	return render_template("index.html", title = "Home", user = user, posts = posts)









