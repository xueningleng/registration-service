import logging.handlers
from flask import Flask, Response, request, redirect
from datetime import datetime
import json
import os
import google_auth
from registration import Registration
from flask_cors import CORS

application = Flask(__name__)
CORS(application)


# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>Registration</title> </head>\n<body> <h2>REGISTRATION PAGE</h2> '''
instructions = '''
    <p><em>Hint</em>: <br>
    Append '/api/health' to the URL to test connectivity<br>
    </p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'
login_btn = '''
<a class="button" href="/google/login">Google Login</a>'''
logout_btn = '''
<a class="button" href="/google/logout">Logout</a>'''

application.register_blueprint(google_auth.app)
application.secret_key = os.environ.get("FLASK_SECRET_KEY", default=False)

@application.before_request
def load_user():
    if not google_auth.is_logged_in() and request.endpoint in ('check_registration', 'google_logout'):
        print("user not logged in")
        return redirect("/")


@application.after_request
def after_request_func(response):
    print("request completed")
    return response

@application.route('/',  endpoint='auth')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()

        res = Registration.get_user_record(user_info['email'])
        if res:
            # returning account
            hello_text = "<div> Welcome back " + user_info['given_name'] + " :) <br> You are signed in with email: " + \
                         user_info['email'] + "</div><br>"
        else:
            # not registered yet

            err = Registration.add_user(user_info['email'], user_info['given_name'], user_info['family_name'])
            if not err:
                hello_text = "<div> Hello "+ user_info['given_name'] + "! <br> You are now registered under email: " + \
                    user_info['email'] + "</div><br>"

            else:
                hello_text = "<div> Sorry! Registration failed. Please try again later." + err.args[1] + "</div><br>"

        return header_text + hello_text + logout_btn + footer_text

    return  header_text +'<div>You are not currently logged in. </div>'+ instructions + login_btn + footer_text

@application.get("/api/health", endpoint='health_check')
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "thumbsup-registration",
        "health": "Good",
        "at time": t
    }

    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result

@application.route("/api/check-registration/", methods = ['GET'], endpoint='check_registration')
def check_registration():
    msg = "Existing Registration Records:\n"
    records = Registration.get_users();
    for record in records:
        msg += str(record) + '\n'

    result = Response(msg, status=200, content_type="text/plain")
    return result

if __name__ == '__main__':
    application.debug = True
    application.run(host="0.0.0.0", port=5011)
