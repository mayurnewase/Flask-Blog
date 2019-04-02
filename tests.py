import unittest
from app import app_instance as app, db
from app.models import User,Post



class UserModelCase(unittest.TestCase):
	def setUp(self):
		app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
		db.create_all()


	def tearDown(self):
		db.session.remove()
		db.drop_all()

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


















































