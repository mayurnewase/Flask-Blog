from flask import Blueprint
api_bp = Blueprint("api", __name__)


from app.api import users, errors, tokens



"""
HTTP Method 	Resource URL 			Notes
GET 		/api/users/<id> 	 		Return a user.
GET 		/api/users 					Return the collection of all users.
GET 		/api/users/<id>/followers 	Return the followers of this user.
GET 		/api/users/<id>/followed 	Return the users this user is following.
POST 		/api/users 					Register a new user account.
PUT 		/api/users/<id> 			Modify a user.

"""


"""
{
    "id": 123,
    "username": "susan",
    "password": "my-password",
    "email": "susan@example.com",
    "last_seen": "2017-10-20T15:04:27Z",
    "about_me": "Hello, my name is Susan!",
    "post_count": 7,
    "follower_count": 35,
    "followed_count": 21,
    "_links": {
        "self": "/api/users/123",
        "followers": "/api/users/123/followers",
        "followed": "/api/users/123/followed",
        "avatar": "https://www.gravatar.com/avatar/..."
    }
}
"""