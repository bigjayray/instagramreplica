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

class Profile(webapp2.RequestHandler):
    #get method called by webapp2 in response to HTTP get request
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        #gets current user
        user = users.get_current_user()

        # gets user
        k_str = self.request.get('key')

        muser = ndb.Key(urlsafe=k_str).get()

        posts = muser.posts

        nposts = len(muser.posts)
        nfollowers = len(muser.followers)
        nfollowing = len(muser.following)

        myuser = ndb.Key('User', user.user_id()).get()

        #assign template values to be rendered to the html page
        template_values = {
            'user' : user,
            'posts' : posts,
            'nposts' : nposts,
            'nfollowers' : nfollowers,
            'nfollowing' : nfollowing,
            'get_serving_url' : get_serving_url,
            'myuser' : myuser,
            'muser' : muser
        }

        template = JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))
