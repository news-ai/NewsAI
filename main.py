# Stdlib imports
import logging
from email.utils import parseaddr

# Third-party app imports
from chimpy import chimpy
from validate_email import validate_email
from flask import Flask, request, render_template, jsonify
from google.appengine.ext import ndb

# Initialize Flask
app = Flask(__name__)

# Initialize Mailchimp
API_KEY = '8d3b59fca89a824d683d235d9e682a9d-us13'
LIST_ID = 'c7ff40b080'
chimp = chimpy.Connection(API_KEY)


# Model for User
class User(ndb.Model):
    email = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    number_invited = ndb.IntegerProperty(default=0)
    invited_by = ndb.StringProperty(default='')
    position = ndb.IntegerProperty(default=0)


class Line(ndb.Model):
    name = ndb.StringProperty()
    current_position = ndb.IntegerProperty()


def create_new_line():
    new_line = Line()
    new_line.name = 'tabulae'
    new_line.current_position = 100
    new_line.put()


def get_curent_position_and_append():
    q = Line.query(Line.name == 'tabulae').get()
    if q is not None:
        current_position = q.current_position
        q.current_position += 1
        q.put()
        return current_position
    return 100


def get_invite_user(user_id):
    # Filter user
    user = User.get_by_id(id=int(user_id))
    # If the user does not exist then return it
    if user:
        # If the user exists then append the number of people they have invited
        user.number_invited += 1
        user.put()
        return user.key.id()
    return ''


def add_new_user(email, invited_by):
    new_user = User()
    new_user.number_invited = 0
    new_user.position = get_curent_position_and_append()
    new_user.email = email

    if invited_by:
        new_user.invited_by = str(invited_by)

    new_user.put()
    return new_user.key.id()


@app.route('/a/position/<user_id>', methods=['GET'])
def get_position(user_id):
    user = User.get_by_id(id=int(user_id))
    if user is None:
        return jsonify({'error': 'user_id is invalid'})
    return jsonify({'position': user.position})


@app.route('/a/subscribe', methods=['POST', 'GET'])
def subscribe():
    if request.method == 'POST':
        # Parse email
        email = request.form['EMAIL']
        invite_code = request.form['INVITE']
        email = parseaddr(email)
        if len(email) > 1 and email[1] != '' and validate_email(email[1]):
            user_unique_id = ''

            if invite_code:
                invite_code = get_invite_user(invite_code)
            else:
                invite_code = ''
            try:
                # Email does not exist in Mailchimp
                chimp.list_subscribe(
                    LIST_ID, email[1], {'FIRST': '', 'LAST': ''}, double_optin=False)
                user_unique_id = add_new_user(email[1], invite_code)
                # Add to datastore & return unique ID
            except chimpy.ChimpyException:
                # Email already exists in Mailchimp
                # now get it from datastore
                q = User.query(User.email == email[1]).get()
                if q is None:
                    # If can't find the user then add them to our platform
                    user_unique_id = add_new_user(email[1], invite_code)
                else:
                    # If they are there then get their unique id
                    user_unique_id = q.key.id()
                # Render template
            return render_template('subscribe.html', unique_id=user_unique_id)

        # Means that the email is invalid. We tell the user
        return render_template('subscribe.html', error='Email is invalid!', unique_id='')

    # If it is any other method but POST
    return render_template('subscribe.html', unique_id='')


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
