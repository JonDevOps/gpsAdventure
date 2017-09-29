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
import json
import urllib
from google.appengine.ext import ndb
from google.appengine.api import users

WEB_SERVICE_BASE = "http://gpsadventure-dreamersnet.appspot.com"
    
class UserPrefs(ndb.Model):
    userid= ndb.StringProperty()    
    nickname = ndb.StringProperty()
    email = ndb.StringProperty()
    def __dict__(self):
        return json.dumps(self.to_dict())
    def serialize(self):
        return json.dumps(self.to_dict(), default = lambda (o): o.__dict__)
    def setNickname(self,nickname):
        self.nickname = nickname
    def setEmail(self,email):
        self.email = email
    def setAll(self,userid,nickname,email):
        self.userid= userid
        self.nickname= nickname
        self.email= email
    @classmethod
    def db_create(cls,userid):
        nUser = UserPrefs()        
        q = ndb.gql("SELECT * FROM UserPrefs WHERE userid = :1", userid)
        tmp = q.get()
        if tmp:
            nUser.setAll(userid, tmp.nickname, tmp.email)
        else:
            nUser.setAll(userid,"Anonymous","unknown")
            nUser.put()
        return nUser
    def create(cls,userid,nickname,email):
        nUser = UserPrefs()
        dirty = False
        nUser.setAll(userid, nickname, email)
        q = ndb.gql("SELECT * FROM UserPrefs WHERE userid = :1", nUser.userid)
        tmp = q.get()
        if tmp:
            if tmp.nickname != nUser.nickname:
                nUser.setNickname(tmp.nickname)
                dirty = True
            if tmp.email != nUser.email:
                nUser.setEmail(tmp.email)
                dirty = True
        else:
            dirty = True
        if dirty:  #or needs update
            nUser.put()
        return nUser
    def query_userpref(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key)
    def form(cls):
        userForm = """\
        <html>
        <body> 
        <form action='""" + \
        WEB_SERVICE_BASE + \
        """/userpref' method="post">
          <table>
          <tr>
          <td>User ID: </td> <td><input type="hidden" id="userid" name="userid" value='""" + \
          self.userid + \
          """'></input> </td>
          <td>Nickname: </td> <td><input id="Nickname" name="Nickname" value'"""+ \
          self.nickname + \
          """'></input> </td>
          </tr> <tr>
          <td>Email:</td> <td> <input id="Email" name="Email" value='""" + \
          self.email + \
          """' readonly="readonly"></input></td>
          </tr> <tr>
          <td></td><td><input type="submit" value="Save"></td>
          </tr>
        </form>
        </body>
        </html>
        """
        return userForm
    
