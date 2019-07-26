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
import time

from models import Item

from google.appengine.api import users


jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ItemHandler(webapp2.RequestHandler):
    def get(self):
        my_user = users.get_current_user()
        start_page = jinja_current_dir.get_template("templates/posts.html")
        self.response.write(start_page.render())

    def post(self):
        the_post = self.request.get('title')
        the_caption = self.request.get('caption')
        the_image = self.request.get('image_url')
            #put into database (optional)
        item = Item(title = the_post, caption = the_caption, image_url = the_image)
        item.user_id = users.get_current_user().user_id()
        item.put()
        time.sleep(0.1)
        self.redirect("/")

class MainPage(webapp2.RequestHandler):
    def get(self):
        main_temp = jinja_current_dir.get_template("templates/welcome.html")
        my_user = users.get_current_user()

        if my_user:
            auth_url = users.create_logout_url('/') #goes back to main page when logged out
            greeting = 'Welcome! Sign Out'
        else:
            auth_url = users.create_login_url('/')
            greeting = 'Sign In'
        # [END user_details]
        items = Item.query().fetch()
        your_items = Item.query().filter(Item.user_id == my_user.user_id()).order(-Item.title).fetch()
        others_items = Item.query().order(-Item.title).fetch()

        my_dict = {
            'auth_url': auth_url,
            'greeting': greeting,
            'your_own_items': your_items,
            'everyones_items': others_items,
        }
        self.response.write(main_temp.render(my_dict))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/new-post', ItemHandler)
], debug=True)
