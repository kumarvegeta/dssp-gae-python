# -*- coding: utf-8 -*-

# [START gae_flex_quickstart]

import logging
import cgi
import gensim

import os
import flask
import google.oauth2.credentials
import googleapiclient.discovery
import google_auth_oauthlib.flow

import random
from numpy.linalg import norm
import json, glob
import re, math, operator
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = flask.Flask(__name__)
app.secret_key = 'dsspp_secret_key'


# OAuth
CLIENT_SECRETS_FILE = "resources/client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/userinfo.profile"]


@app.route("/authorize", methods=['POST'])
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    flask.session['state'] = state
    return flask.redirect(authorization_url)


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    return flask.redirect("/")


@app.route('/logout', methods=["GET", "POST"])
def logout():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    return flask.redirect("/")


@app.route('/hello')
def hello():
    """Return a friendly HTTP greeting."""
    return flask.render_template("hello.html")


@app.route('/')
def main():
    if 'credentials' not in flask.session:
        return flask.render_template("login.html")
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])
    oauth2_api = googleapiclient.discovery.build(
      "oauth2", "v2", credentials=credentials)
    try:
        user = oauth2_api.userinfo().v2().me().get().execute()['name']
        return flask.render_template("main.html", user=user)
    except Exception:
        return flask.redirect(flask.url_for("logout"))


@app.route('/search', methods=["POST"])
def search():
    if 'credentials' not in flask.session:
        return flask.redirect("/")
    language = flask.request.form.get('language')
    domain = flask.request.form.get('domain')
    word = flask.request.form.get(cgi.escape('word'))
    resource_path = "resources/%s_%s.w2v" % (language, domain)
    if not os.path.exists(resource_path):
        error_message = "Model not found for Language: <b>%s</b> and Domain: <b>%s</b>" % (language, domain)
        return flask.render_template("error.html", error=flask.Markup(error_message))
    model = gensim.models.Word2Vec.load(resource_path)
    try:
        results = model.most_similar(word)
    except KeyError:
        results = None
    success_template = "results_en.html" if language == "English" else "results_es.html"
    failure_template = "failure_en.html" if language == "English" else "failure_es.html"
    if results and len(results) > 0:
        create_plot(word, results)
        rendered = ""
        for result in results:
            rendered += "<tr><td>%s</td><td>%0.8f</td></tr>" % (result[0], result[1])
        image_path = "/static/results.png?dummy=%d" % random.randint(0, 1000)
        return flask.render_template(success_template, word=word, results=flask.Markup(rendered), image_path=image_path)
    else:
        return flask.render_template(failure_template, word=word)


def create_plot(word, results):
    if os.path.exists("static/results.png"):
        os.remove("static/results.png")
    x = range(1, len(results) + 1)
    y = [r[1] for r in results]
    plt.plot(x, y)
    plt.ylabel('Cosine Similarities')
    plt.title("Word indices for '%s' in decreasing order of cosine similarity" % word)
    plt.xlabel('Word Index')
    plt.savefig("static/results.png")
    plt.clf()


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
