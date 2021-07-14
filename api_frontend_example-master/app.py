
# TTP API Frontend Example
# Version 1.0 20210714
# by Johnnie Odom 

# Basic imports used in this application.
from flask import Flask, Response, request, redirect, session, json, jsonify
from threading import Thread
import os.path
import requests
# Session management. Chosen because it encrypts and offers multiple backends.
from flask_session import Session
from datetime import timedelta  # Used by our configuration for session.
# The following should be the name of the config file which contains our OAuth information among other things.
import example_config

# Hardcoded application configuration.
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
# Change when we know a reasonable default.
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
# Assuming every one of our users gets one ...
app.config['SESSION_FILE_THRESHOLD'] = 50000
# Replace with config.SECRET_KEY when we have one.
app.config['SECRET_KEY'] = '123456789'
app.config['SESSION_FILE_DIR'] = '.session_data'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Session information. This is provided for user convenience but we only trust the OAuth value from it.
Session(app)



@app.route('/')
def newdefault():
    oauth_code = ''
    # Try logging in with new OAuth code.
    if 'code' in request.args and 'state' in request.args:
        oauth_code = request.args.get('code')
        jsondata = example_config.NamRetrieveToken(oauth_code)
        # Make this conditional on a successful json return.
        session['token'] = jsondata['access_token']
        return redirect(example_config.localurl + '/')
    elif session.get('token'):  # Look for Oauth key in session
        token = session.get('token')
        return TestApiCalls(token)
    else:  # Redirect to OAuth login and create new session.
        return redirect(example_config.oauthurl + '/nidp/oauth/nam/authz?response_type=code&client_id=' + example_config.clientid + '&redirect_uri=' + example_config.localurl + '/&scope=' + example_config.scopewanted + '&nonce=' + example_config.nonce + '&state=' + example_config.state)

def TestApiCalls(tokencopy):
    currentUrlToTest = example_config.apiurl +  '/ttp/tokeninfo'
    #apir = requests.get(currentUrlToTest, verify=False)
    #myheaders={'Content-type':'text/plain', 'Accept':'text/plain'}
    apir = requests.post(currentUrlToTest, json = {"enctoken" : tokencopy}, verify = False)
    stringReturn = '<!DOCTYPE html>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">\n<html>\n	<head>\n		<title>Example Frontend Application</title>\n		<link rel="stylesheet" href="static/css/main.css">\n	</head>\n	<body>\n		<div id="feedback" class="notice">\n </div>\nYour email is: <a href="mailto:' + str(apir.json()) + '"/>' + str(apir.json()) + '</a>' + '	</body>\n</html>\n'
    return stringReturn
