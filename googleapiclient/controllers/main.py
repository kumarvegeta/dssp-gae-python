#!/usr/bin/python
# -*- coding: UTF-8 -*-

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
"""Starting template for Google App Engine applications.

Use this project as a starting point if you are just beginning to build a Google
App Engine project. Remember to download the OAuth 2.0 client secrets which can
be obtained from the Developer Console <https://code.google.com/apis/console/>
and save them as 'client_secrets.json' in the project directory.
"""

__author__ = 'jcgregorio@google.com (Joe Gregorio)'

import cgi
import httplib2
import logging
import os
import pickle
import webapp2
import webob
import os

from controllers.base import BaseHandler
from apiclient.discovery import build
#from oauth2client.appengine import oauth2decorator_from_clientsecrets
from oauth2client.contrib.appengine import oauth2decorator_from_clientsecrets
from oauth2client.client import AccessTokenRefreshError
from google.appengine.api import memcache

#from flask import Flask, request, redirect, render_template

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(os.path.dirname(__file__)),
    'client_secrets.json')

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
<h1>Warning: Please configure OAuth 2.0</h1>
<p>
To make this sample run you will need to populate the client_secrets.json file
found at:
</p>
<p>
<code>%s</code>.
</p>
<p>with information found on the <a
href="https://code.google.com/apis/console">APIs Console</a>.
</p>
""" % CLIENT_SECRETS


http = httplib2.Http(memcache)
service = build("plus", "v1", http=http)
decorator = oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    'https://www.googleapis.com/auth/plus.me',
    MISSING_CLIENT_SECRETS_MESSAGE)

class MainHandler(BaseHandler):

  @decorator.oauth_aware
  def get(self):
    variables = {
        'url': decorator.authorize_url(),
        'has_credentials': decorator.has_credentials()
        }
    self.render_response('grant.html', **variables)


class IndexHandler(BaseHandler):

  @decorator.oauth_required
  def get(self):
    try:
      http = decorator.http()
      user = service.people().get(userId='me').execute(http)
      text = 'Hello, %s!' % user['displayName']

      self.render_response('welcome.html', text=text)

      #render_template('dsspp_main.html')
    except AccessTokenRefreshError:
      self.redirect('/')


def SelectionPage(request):
    #return webapp2.Response("index.html")
    return webapp2.Response("""<!doctype html>
<html lang="en">
 <head> <meta charset="utf-8">
   <title>D.S.S.P.P. On Python for GAE</title>
 </head>
 <body>
   <h1>Welcome to the DSSPP. Please choose your language:</h1>
   <form action="proc_form" method="POST">
     <table>
       <tr>
         <th>Language:</th>
         <td>English<input type="radio" name="language" value="English" checked="yes" /><br />
           Spanish<input type="radio" name="language" value="Spanish" /><br />
         </td>
       </tr>
     </table>
     <input type="submit" value="Submit" />
   </form>
 </body>
</html>""")

def proc_form(request):

    language = request.params.get(cgi.escape('language'))
    if language == "English":
        return webapp2.Response(""" <!doctype html>
<html lang="en">
<head>  <meta charset="utf-8">
<title> D.S.S.P.P. On Python For GAE </title>
</head>
  <body>
        <h3>Enter the word in English to find similar words for:</h3>
        <form method="GET" action="eng_results">
          <input type="text" name="word_string"><br />
          <input type="submit" name ="Submit">
        </form>
  </body>
</html>
 """)
    if language =="Spanish":
        return webapp2.Response(""" <!doctype html>
<html lang="es">
<head> <meta charset="utf-8">
<title> D.S.S.P.P. En Python para GAE </title>
</head>
  <body>
        <h3> Ingrese la palabra en español para encontrar palabras similares para: </h3> 
         <form method="GET" action="esp_results">
          <input type="text" name="word_string"><br />
          <input type="submit" name ="Enviar">
        </form>
  </body>
</html>
 """)

app = webapp2.WSGIApplication(
    [
     ('/', MainHandler),
     ('/MainPage', IndexHandler),

     ('/selection', SelectionPage),
     #('/images/eng_results', render_image),
     #('/images/esp_results', render_es_image),
     ('/proc_form', proc_form),
     #('/eng_results',eng_results),
     #('/esp_results',esp_results),
     (decorator.callback_path, decorator.callback_handler())
    ],
    debug=True)
