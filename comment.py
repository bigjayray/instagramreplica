import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api.images import get_serving_url
import os

from model import User
from model import Comments

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Comment(webapp2.RequestHandler):
    #get method called by webapp2 in response to HTTP get request
    def post(self):
        self.response.headers['Content-Typ'] = 'text/html'

        # form values
        post_k_str = self.request.get('post')
        post_key = ndb.Key(urlsafe=post_k_str)
        post = post_key.get()

        # gets key
        k_str = self.request.get('key')
        key = ndb.Key(urlsafe=k_str)

        # creates new comment object
        new_comment = Comments()

        #updates comment attributes
        new_comment.comment = self.request.get('comment')
        new_comment.user = key

        post.comments.append(new_comment)

        # updates post
        post.put()

        self.redirect('/')
