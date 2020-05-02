import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from model import User

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Followers(webapp2.RequestHandler):
    #get method called by webapp2 in response to HTTP get request
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        #gets current user
        user = users.get_current_user()

        # gets user key
        k_str = self.request.get('key')
        key = ndb.Key(urlsafe=k_str)

        # gets user
        muser = key.get()

        #gets list of followers
        followers = muser.followers

        myuser = ndb.Key('User', user.user_id()).get()

        #assign template values to be rendered to the html page
        template_values = {
            'user' : user,
            'myuser' : myuser,
            'muser' : muser,
            'followers' : followers
        }

        template = JINJA_ENVIRONMENT.get_template('followers.html')
        self.response.write(template.render(template_values))
