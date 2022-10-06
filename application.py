import logging.handlers
from flask import Flask, Response, request
from datetime import datetime
import json
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
    Append '/api/register/?phone=value&first_name=value&last_name=value&password=value' to the URL with your own value to register!<br>
    Append '/api/check-registration/' to the URL to view existing records by contact and name<br>
    </p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
instructions + footer_text))

@application.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "thumbsup-registration",
        "health": "Good",
        "at time": t
    }

    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result

@application.route("/api/register/", methods = ['GET', 'POST'])
def register():
    # ?phone=value&first_name=value&last_name=value&password=value
    # test: {ENDPOINT}/api/register/?phone=2223330000&first_name=foo&last_name=bar&password=88888888
    phone = request.args.get('phone', type=str)
    fname = request.args.get('first_name', type=str)
    lname = request.args.get('last_name', type=str)
    pword = request.args.get('password', type=str)
    msg = {
        "phone" : phone,
        "name" : fname+" "+lname,
        "pword" : "*"*len(pword),
    }

    err = Registration.add_user(phone, fname, lname, pword);
    if not err:
        msg["result"]= "Registration succeeded!"
        result = Response(json.dumps(msg), status=200, content_type="application/json")

    else:
        result = Response(err.args[1], status=404, content_type="text/plain")


    return result

@application.route("/api/check-registration/", methods = ['GET', 'POST'])
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
