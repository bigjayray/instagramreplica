#imports
from google.appengine.ext import ndb

#User class
class User(ndb.Model):
    # A model for representing a user
    #user attributes
    email_address = ndb.StringProperty()
    following = ndb.KeyProperty(kind='User', repeated=True)
    followers = ndb.KeyProperty(kind='User', repeated=True)
    posts = ndb.KeyProperty(kind='Posts', repeated=True)

class Posts(ndb.Model):
    # A model for representing a post
    #posts attributes
    image = ndb.BlobKeyProperty()
    caption = ndb.StringProperty()
    comments = ndb.StringProperty()
    user = ndb.KeyProperty(kind='User')
    create_date = ndb.DateTimeProperty(auto_now_add=True)
