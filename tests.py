import unittest
from app import db
from app.models import User,Post
from config import Config
from app import create_app

class TestConfig(Config):
	SQLALCHEMY_DATABASE_URI = "sqlite://"

class UserModelCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app(TestConfig)

		#now push app context why,
		#because imported db instance is empty,
		#it needs app_instance to use db_uri from app.config
		#so now app_instance is not available as global variable,
		#so how does it automatically know which app_instance to use?
		#from application context -> current_app -> proxy for app_instance
		#current_app looks for active application context in current_thread,which was pushed by flask
		
		self.app_context = self.app.app_context()
		self.app_context.push()
		#now application context and current_app is available
		
		db.create_all()   #create table


	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_password_hashing(self):
		u1 = User(name = "mia")
		u1.set_password("big")

		self.assertFalse(u1.check_password("small"))
		self.assertTrue(u1.check_password("big"))

	def test_adding_post(self):
		u1 = User(name = "sunny")
		u2 = User(name = "india")

		p1 = Post(body="test_post1", author = u1)

		p2 = Post(body="test_post2", author = u2)
		p3 = Post(body="test_post3", author = u2)

		db.session.add_all([u1,u2,p1,p2])
		db.session.commit()

		u1_posts = u1.posts.all()
		u2_posts = u2.posts.all()

		all_users = len(User.query.all())  #test user added

		self.assertEqual(all_users, 2)
		self.assertEqual(u1_posts, [p1])
		self.assertEqual(u2_posts, [p2, p3])


if __name__ == "__main__":
	unittest.main(verbosity=2)


















































