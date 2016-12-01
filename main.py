# Stdlib imports
import logging
from email.utils import parseaddr

# Third-party app imports
import urllib2 as urllib
from flask import Flask, request, render_template, jsonify
from google.appengine.ext import ndb

# Initialize Flask
app = Flask(__name__)

@app.route('/a/subscribe', methods=['GET'])
def subscribe():
    return render_template('subscribe.html')


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
