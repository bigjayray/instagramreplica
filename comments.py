#imports
from google.appengine.ext import ndb

class Comments(ndb.Model):
    # A model for representing a comment
    #comment attributes
    comment = ndb.StringProperty()
    create_date = ndb.DateTimeProperty(auto_now_add=True)
    user = ndb.KeyProperty(kind='User')
