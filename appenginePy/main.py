#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from UserPref import *
from missions import Mission, Event
from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator
from google.appengine.ext import ndb
from decimal import Decimal
import cgi

decorator = OAuth2Decorator(
  client_id='474832205158-5q0sqta9e932cmftub9aaihgeb2c6hko.apps.googleusercontent.com',
  client_secret='Tak7Olo_Wa48isvxf1wM7KE4',
  scope='https://www.googleapis.com/auth/userinfo.email')

service = build
WEB_SERVICE_BASE = "http://gpsadventure-dreamersnet.appspot.com"
    
       
class myDataStore:
    def getMissions(self):
        return Mission.query().fetch()


class MissionHandler(webapp2.RequestHandler):
    def get(self):
        if (self.request.get('Title')):
            searchTitle = cgi.escape(self.request.get('Title'))
        else:
            searchTitle = "*"  #return all
        m = Mission.query(Mission.title==searchTitle).fetch()
        self.response.headers['Access-Control-Allow-Origin'] = 'http://gpsadventure.dreamersnet.net'
        self.response.headers['Content-Type'] = 'application/json'
        if (len(m) == 1):
            self.response.write(m[0].serialize())
        else:
            self.response.write("Error 404 Mission not found.")
    @decorator.oauth_required
    def post(self):
        newTitle = cgi.escape(self.request.get('Title'))
        lon = cgi.escape(self.request.get('Longitude'))
        lat = cgi.escape(self.request.get('Latitude'))
        newDesc = cgi.escape(self.request.get('Desc'))
        creatorName = cgi.escape(self.request.get('Creator'))
        userPref = UserPrefs().db_create(users.get_current_user().user_id())
        if creatorName!=userPref.nickname:
            userPref = null
        matches = Mission.query(Mission.title==newTitle).fetch()
        if (len(matches) > 0):
            return;
        m = Mission(position = [ ndb.GeoPt(lat,lon)],title=newTitle,desc=newDesc, creator=userPref)
        missions = myDataStore().getMissions()
        missions.append(m)
        self.response.headers['Access-Control-Allow-Origin'] = 'http://gpsadventure.dreamersnet.net'
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(m.serialize())
        for mission in missions:
            mission.put()

class MissionsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = 'http://gpsadventure.dreamersnet.net'
        self.response.headers['Content-Type'] = 'application/json'
        numMissions = len(myDataStore().getMissions())
        ct = 0
        self.response.write("[")
        for m in myDataStore().getMissions():
            ct +=1
            self.response.write(m.serialize())
            if (ct<numMissions):
                self.response.write(",")
        self.response.write("]")

class MissionFormHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = 'http://gpsadventure.dreamersnet.net'
        self.response.headers['Content-Type'] = 'text/html'
        searchTitle = cgi.escape(self.request.get('Title'))
        matches = Mission.query(Mission.title==searchTitle).fetch()
        if (len(matches) > 1):
            return;
        elif (len(matches) == 0):
            self.response.write(Mission().form()) 
        else:
            m=matches[0];
            self.response.write(m.getForm())
            

class WaypointHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def post(self):
        self.response.headers['Access-Control-Allow-Origin'] = 'http://gpsadventure.dreamersnet.net'
        self.response.headers['Content-Type'] = 'application/json'
        searchTitle = cgi.escape(self.request.get('Title'))
        lon = cgi.escape(self.request.get('Longitude'))
        lat = cgi.escape(self.request.get('Latitude'))
        m = Mission.query(Mission.title==searchTitle).fetch()
        if (len(m) == 1):
            m[0].addWaypoint(lat,lon)
            self.response.write(m[0].serialize)
        
class WhoamiHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = 'http://gpsadventure.dreamersnet.net'
        self.response.headers['Content-Type'] = 'application/json'
        user = users.get_current_user()
        self.response.write("{ " + user.user_id() + "," + user.nickname() + "," + \
                            repr(user.email()) + "}")
        if user:
            q= ndb.gql("SELECT * FROM UserPrefs WHERE userid = :1", user.user_id())
            userprefs = q.get()
            if userprefs:
                self.response.write('DB:' + repr(userprefs))
            else:
                newUser = UserPrefs().create(user.user_id(), user.nickname(), user.email())
                newUser.put()
        
class UserFormHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = 'http://gpsadventure.dreamersnet.net'
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(UserPrefs().db_create(users.get_current_user().user_id()).form())
    def post(self):
        userid = cgi.escape(self.request.get('userid'))
        nickname = cgi.escape(self.request.get('Nickname'))
        email = cgi.escape(self.request.get('Email'))
        user = UserPref(userid,nickname,email)

class UserPrefHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = 'http://gpsadventure.dreamersnet.net'
        self.response.headers['Content-Type'] = 'application/json'
        user = UserPrefs().db_create(users.get_current_user().user_id())
        self.response.write(user.serialize())
        
    
class MainHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = 'http://gpsadventure.dreamersnet.net'
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/missionForm', MissionFormHandler),
    ('/missions', MissionsHandler),
    ('/mission', MissionHandler),
    ('/waypoint', WaypointHandler),
    ('/whoami', WhoamiHandler),
    ('/userForm', UserFormHandler),
    ('/userpref', UserPrefHandler),
    (decorator.callback_path, decorator.callback_handler()),
], debug=True)
