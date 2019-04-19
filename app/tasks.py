"""
this is used for background tasks
this will use application context, db, user info
so this need
	app context
	db access

when we do flask run blog.py create app -> but background task doesn't know it and can't access it

so it need to create its own app and push context to make current_app accessible
so if any task need current task it can use it.

so import all that shit like blog.py do at top level.

"""
from app import create_app, db
from rq import get_current_job
from app.models import User, Post, Task
from app.email import send_mail

import json
import sys
import time
from flask import render_template



exporter_app = create_app()
exporter_app.app_context().push()

def _set_task_progress(progress):
	#used to upfate progress of currently executig task and update progress in db
	#notification is added to the user who requested this task

	job = get_current_job()  #get currently executing job from queue -> WHAT IF MULTIPLE JOBS EXECUTING
							#HOW TO GET JOB RUNNING FOR SPECIFIC USER
	if job:
		job.meta["progress"] = progress
		job.save_meta()
		task = Task.query.get(job.get_id())   #get object of that job form id
												#why get not filter().first()
		task.user.add_notification("task_progress", {"task_id": job.get_id(), "progress" : progress})

		if progress > 100:
			task.complete = True

		db.session.commit()   #this will commit and not main app


def export_posts(user_id):
	#read user posts
	#send email with data
	#handle errors

	try:

		user = User.query.get(user_id)    #WHY GET,WHY NOT FILTER_BY().FIRST()
		_set_task_progress(0)
		data = []
		i = 0
		total_posts = user.posts.count()   #WHAT IS COUNT HERE ?

		for index, post in enumerate(user.posts.order_by(Post.timestamp.asc())):
			data.append({"body" : post.body, "timestamp" : post.timestamp.isoformat() + "Z"})

			time.sleep(5)

			_set_task_progress((i / total_posts) * 100)

		send_mail(subject = "blogs exporter", 
			sender = exporter_app.config["ADMINS"][0],
			reciever =exporter_app.config[user.mail],
			text = "Posts are exporterd",
			html = None,
			attatchments = json.dumps({"posts": data}, indent = 4),
			sync = True)   #send in foreground

	except:
		#call app logging module -> currently not defined
		#but if error happens here flask wont tell you
		#you will only know if you are watching task terminal constantly
		_set_task_progress(100)

















