#imports
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api.images import get_serving_url
import os
import itertools

from model import User
from model import Posts
from createpost import CreatePost
from uploadhandler import UploadHandler
from profile import Profile
from search import Search
from follow import Follow
from followers import Followers
from following import Following


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

#MainPage class
class MainPage(webapp2.RequestHandler):
    #get method called by webapp2 in response to HTTP get request
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        #initializing variables
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        myuser = None
        posts = []

        #gets current user
        user = users.get_current_user()

        #selection for user
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            #gets user key
            myuser_key = ndb.Key('User', user.user_id())

            #generates user from key
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = User(id=user.user_id())
                #adds mail attribute
                myuser.email_address = user.email()
                #saves user to datastore
                myuser.put()

            for i in myuser.following:
                q = Posts.query().filter(Posts.user == i).fetch()
                for i in q:
                    posts.append(i)
            for i in myuser.posts:
                posts.append(i.get())


        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'


        #assign template values to be rendered to the html page
        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'myuser' : myuser,
            'posts' : posts,
            'get_serving_url' : get_serving_url
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


# specify the full routing table
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/createpost', CreatePost),
    ('/upload', UploadHandler),
    ('/profile', Profile),
    ('/search', Search),
    ('/follow', Follow),
    ('/followers', Followers),
    ('/following', Following)
], debug=True)
