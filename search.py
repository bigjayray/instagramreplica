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

class Search(webapp2.RequestHandler):
    #get method called by webapp2 in response to HTTP get request
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        #gets current user
        user = users.get_current_user()
        myuser = ndb.Key('User', user.user_id()).get()

        #assign template values to be rendered to the html page
        template_values = {
            'user' : user,
            'myuser' : myuser
        }

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):

        #gets current user
        user = users.get_current_user()

        #gets user key
        myuser_key = ndb.Key('User', user.user_id())

        #generates user from key
        myuser = myuser_key.get()

        # get value of button clicked
        action = self.request.get('button')

        # selection statement for if add user button is clicked
        if action == 'Search':

            # gets form values
            username = self.request.get('username')

            #querys data store to find all users
            result = User.query().filter(User.email_address == username).fetch()

            error = False
            if result == []:
                error = True

            #gets current user
            myuser = ndb.Key('User', user.user_id()).get()

            #assign template values to be rendered to the html page
            template_values = {
                'user' : user,
                'result' : result,
                'myuser' : myuser,
                'error' : error
            }

            template = JINJA_ENVIRONMENT.get_template('search.html')
            self.response.write(template.render(template_values))
