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
import json
import urllib
from UserPref import *
from google.appengine.ext import ndb
from google.appengine.api import users

userPref = UserPrefs().db_create(users.get_current_user().user_id())

WEB_SERVICE_BASE = "http://gpsadventure-dreamersnet.appspot.com"
MISSION_FORM_HTML = """
<html>
  <body> 
    <form action='""" + \
    WEB_SERVICE_BASE + \
    """/mission' method="post">
      <table>
      <tr>
      <td>Title: </td> <td><input id="MissionTitle" name="Title"></input></td>
      </tr> <tr>
      <td>Longitude:</td> <td> <input id="MissionLon" name="Longitude"></input></td>
      </tr> <tr>
      <td>Latitude: </td> <td> <input id="MissionLat" name="Latitude"></input></td>
      </tr> <tr>
      <td>Description: </td><td><textarea name="Desc"></textarea></td>       
      </tr> <tr>
      <td>Creator: </td><td> <input id="Creator" name="Creator" value='""" + \
      userPref.nickname + \
        """' readonly="readonly"></input></td></tr>
      <td></td><td><input type="submit" value="Add Mission"></td>
      </tr>
    </form>
  </body>
</html>
""" 
    
class Mission(ndb.Model):
    position = ndb.GeoPtProperty(repeated=True)
    title = ndb.StringProperty()
    desc = ndb.StringProperty()
    creator = ndb.StructuredProperty(UserPrefs)
    def serialize(self):
        return json.dumps(self.to_dict(), default = lambda (o): o.__dict__)
    def addWaypoint(self,lat,lon):
        p1= ndb.GeoPt(lat,lon)
        self.position = self.position + [p1]
        self.put()
    def getForm(self):
        if (len(self.title) > 0):
            form_Response = """\
            <html>
              <body>
                <form action='""" + \
                WEB_SERVICE_BASE + """/waypoint' method="post">
                  <table>
                  <tr>
                  <td>Title: </td> <td><input id="MissionTitle" name="Title" value='""" + \
                  self.title + \
                  """' readonly="readonly"></input></td>
                  </tr> <tr>
                  <td>Longitude:</td> <td> <input id="MissionLon" name="Longitude"></input></td>
                  </tr> <tr>
                  <td>Latitude: </td> <td> <input id="MissionLat" name="Latitude"></input></td>
                  </tr> <tr>
                  <td>Creator: </td><td> <input id="Creator" name="Creator" value='""" + \
                    userPref.nickname + \
                    """' readonly="readonly"></input></td></tr>
                  <td></td><td><input type="submit" value="Add Waypoint"></td>
                  </tr>
                </form>
              </body>
            </html>
            """
            return form_Response
        else:
            return MISSION_FORM_HTML
    @classmethod
    def query_mission(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key)
    def form(cls):
        return MISSION_FORM_HTML
   
class Event(ndb.Model):
    time = ndb.DateTimeProperty()
    mission = ndb.StringProperty()
    def serialize(self):
        return json.dumps(self.to_dict(), default = lambda (o): o.__dict__)
