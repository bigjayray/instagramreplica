import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api.images import get_serving_url
import os

from model import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Follow(webapp2.RequestHandler):
    #get method called by webapp2 in response to HTTP get request
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        #gets current user
        user = users.get_current_user()

        # gets keys
        k_str_me = self.request.get('me')
        k_str_you = self.request.get('you')

        key_me = ndb.Key(urlsafe=k_str_me)
        key_you = ndb.Key(urlsafe=k_str_you)

        #updates following/followers
        me = key_me.get()
        me.following.append(key_you)

        you = key_you.get()
        you.followers.append(key_me)

        #updates users
        me.put()
        you.put()

        self.redirect('/profile?key='+k_str_you)
