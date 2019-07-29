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
from google.appengine.ext import ndb
from google.appengine.api import users


jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def get_user_info():
    my_user = users.get_current_user()
    if my_user:
        auth_url = users.create_logout_url('/') #goes back to main page when logged out
        greeting = 'Welcome! Sign Out'
    else:
        auth_url = users.create_login_url('/')
        greeting = 'Sign In'
    return my_user, auth_url, greeting



class DetailItemHandler(webapp2.RequestHandler):
    def get(self):
        main_temp = jinja_current_dir.get_template("templates/details.html")
        my_user, auth_url, greeting = get_user_info()

        item_key_string = self.request.get("item")
        item_key = ndb.Key(urlsafe=item_key_string)
        item = item_key.get()


        my_dict = {
            'auth_url': auth_url,
            'greeting': greeting,
            'item':item

        }
        self.response.write(main_temp.render(my_dict))

class MyPostsHandler(webapp2.RequestHandler):
    def get(self):
        main_temp = jinja_current_dir.get_template("templates/my-posts.html")
        my_user, auth_url, greeting = get_user_info()
        # [END user_details]
        items = Item.query().fetch()
        your_items = Item.query().filter(Item.user_id == my_user.user_id()).order(-Item.created_on).fetch()
        others_items = Item.query().order(-Item.created_on).fetch()

        my_dict = {
            'auth_url': auth_url,
            'greeting': greeting,
            'your_own_items': your_items,
            'everyones_items': others_items,
        }
        self.response.write(main_temp.render(my_dict))

class ItemHandler(webapp2.RequestHandler):
    def get(self):
        start_page = jinja_current_dir.get_template("templates/posts.html")
        my_user, auth_url, greeting = get_user_info()
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
        my_user, auth_url, greeting = get_user_info()

        items = Item.query().fetch()
        your_items = Item.query().filter(Item.user_id == my_user.user_id()).order(-Item.created_on).fetch()
        others_items = Item.query().order(-Item.created_on).fetch()

        my_dict = {
            'auth_url': auth_url,
            'greeting': greeting,
            'your_own_items': your_items,
            'everyones_items': others_items,
        }
        self.response.write(main_temp.render(my_dict))
class AboutUsHandler(webapp2.RequestHandler):
    def get(self):
        aboutuspage = jinja_current_dir.get_template("templates/aboutus.html")
        my_user, auth_url, greeting = get_user_info()

        my_dict = {
            'auth_url': auth_url,
            'greeting': greeting
        }

        self.response.write(aboutuspage.render(my_dict))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/new-post', ItemHandler),
    ('/my-posts', MyPostsHandler),
    ('/details', DetailItemHandler),
    ('/aboutus', AboutUsHandler)
], debug=True)
