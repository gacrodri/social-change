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
from models import Food
from google.appengine.api import users

#remember, you can get this by searching for jinja2 google app engine
jinja_current_dir = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class FoodHandler(webapp2.RequestHandler):
    def get(self):
        start_template = jinja_current_dir.get_template("templates/welcome.html")
        self.response.write(start_template.render())

    def post(self):
        the_fav_food = self.request.get('user-fav-food')

        #put into database (optional)
        food_record = Food(food_name = the_fav_food)
        food_record.put()

        #pass to the template via a dictionary
        variable_dict = {'fav_food_for_view': the_fav_food}
        end_template = jinja_current_dir.get_template("templates/results.html")
        self.response.write(end_template.render(variable_dict))

class ShowFoodHandler(webapp2.RequestHandler):
    def get(self):
        food_list_template = jinja_current_dir.get_template("templates/foodlist.html")
        fav_foods = Food.query().order(-Food.food_name).fetch(3)
        dict_for_template = {'top_fav_foods': fav_foods}
        self.response.write(food_list_template.render(dict_for_template))

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
