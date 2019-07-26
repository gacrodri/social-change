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

from google.appengine.ext import ndb

class Item(ndb.Model):
    user_id = ndb.StringProperty(required =True)
    title = ndb.StringProperty(required=True)
    caption = ndb.StringProperty(required=True)
    image_url = ndb.StringProperty(required=True)

class Profile(ndb.Model):
    nickname = ndb.StringProperty(required=True)
    user_id = ndb.StringProperty()
    joined_on = ndb.DateTimeProperty(auto_now_add=True)
    updated_on = ndb.DateTimeProperty(auto_now=True)
