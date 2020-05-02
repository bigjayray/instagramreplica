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

class Unfollow(webapp2.RequestHandler):
    #get method called by webapp2 in response to HTTP get request
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        #gets current user
        user = users.get_current_user()

        # gets values
        k_str_me = self.request.get('me')
        k_str_you = self.request.get('you')

        key_me = ndb.Key(urlsafe=k_str_me)
        key_you = ndb.Key(urlsafe=k_str_you)

        me = key_me.get()
        index = 0
        for i in me.following:
            if i == key_you:
                del me.following[index]
            index += 1

        you = key_you.get()
        index = 0
        for i in you.followers:
            if i == key_me:
                del you.followers[index]
            index += 1

        me.put()
        you.put()

        self.redirect('/profile?key='+k_str_you)
