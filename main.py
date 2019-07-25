#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import os
import jinja2
from google.appengine.api import users

#remember, you can get this by searching for jinja2 google app engine
1.  Create a page to make an item
  -- should have a form with the fields of the item (title, caption, image)
2.  Create a datastore model for the item (has same fields)
  -- image should be type ndb.BlobProperty (image = ndb.BlobProperty())
3.  Create a NewItemHandler with a get method that renders the page from item #1 ^
4.  Create a ItemHandler with a post method that is going to be called from the form in item #1.
  -- in this handler, we want to create a new Item model with the fields from the form (self.request.get('title'))
  -- then save that item to the database
  -- then redirect the user to the feed page

jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class NewItemHandler(webapp2.RequestHandler):
    def get(self):
        start_page = jinja_current_dir.get_template("welcome.html")
        self.response.write(start_page.render())

class ItemHandler(webapp2.RequestHandler):
    def post(self):


class MainPage(webapp2.RequestHandler):
    def get(self):
        # [START user_details]
        main_temp = jinja_current_dir.get_template("templates/welcome.html")
        my_user = users.get_current_user()

        if my_user:
            auth_url = users.create_logout_url('/') #goes back to main page when logged out
            greeting = 'Sign Out'
        else:
            auth_url = users.create_login_url('/')
            greeting = 'Sign In'
        # [END user_details]
        my_dict = {
            'auth_url': auth_url,
            'greeting': greeting
        }
        self.response.write(main_temp.render(my_dict))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/food', FoodHandler),
    ('/showfavs', ShowFoodHandler)
], debug=True)
