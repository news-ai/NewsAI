# Stdlib imports
import logging
from email.utils import parseaddr

# Third-party app imports
import sendgrid
import urllib2 as urllib
from chimpy import chimpy
from validate_email import validate_email
from flask import Flask, request, render_template, jsonify
from google.appengine.ext import ndb
from sendgrid.helpers.mail import Email, Content, Substitution, Mail

# Initialize Flask
app = Flask(__name__)

# Initialize Mailchimp
API_KEY = '8d3b59fca89a824d683d235d9e682a9d-us13'
LIST_ID = 'c7ff40b080'
chimp = chimpy.Connection(API_KEY)

# Initialize Sendgrid
SENDGRID_API_KEY = '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'
SENDGRID_SENDER = 'Abhi from NewsAI <abhi@newsai.org>'
sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)


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


def email_interest_email(email, user_code):

    print email
    print user_code

    subject = "Thanks for your interest!"
    to_email = Email(email)
    content = Content("text/html", "Hi!")
    mail = Mail(Email(SENDGRID_SENDER, "Abhi from NewsAI"), subject, to_email, content)
    mail.personalizations[0].add_substitution(
        Substitution("{USER_CODE}", str(user_code)))
    mail.set_template_id("da0f3729-27ba-4ddf-94c7-d7faf4bb26e5")
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
    except urllib.HTTPError as e:
        print e
    return


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

                # Add to datastore & return unique ID
                user_unique_id = add_new_user(email[1], invite_code)

                # This is a new user so send them an email
                email_interest_email(email[1], user_unique_id)
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
            return render_template('subscribe.html', unique_id=user_unique_id, error='')

        # Means that the email is invalid. We tell the user
        return render_template('subscribe.html', unique_id='', error='Email you entered is invalid!')

    # If it is any other method but POST
    return render_template('subscribe.html', unique_id='', error='')


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
