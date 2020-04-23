import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import blobstore
import os

from model import User
from model import Posts

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class CreatePost(webapp2.RequestHandler):
    #get method called by webapp2 in response to HTTP get request
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        #gets current user
        user = users.get_current_user()

        #assign template values to be rendered to the html page
        template_values = {
            'user' : user,
            'upload_url' : blobstore.create_upload_url('/upload')
        }

        template = JINJA_ENVIRONMENT.get_template('createpost.html')
        self.response.write(template.render(template_values))
