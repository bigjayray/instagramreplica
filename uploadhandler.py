import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url
from model import Posts
from model import User

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]

        #gets current user
        user = users.get_current_user()

        #gets user key
        myuser_key = ndb.Key('User', user.user_id())

        #generates user from key
        myuser = myuser_key.get()

        post = Posts()

        post.image = upload.key()
        post.caption = self.request.get('caption')
        post.user = myuser_key
        post_key = post.put()

        myuser.posts.append(post_key)

        myuser.put()

        self.redirect('/profile?key='+myuser_key.urlsafe())
