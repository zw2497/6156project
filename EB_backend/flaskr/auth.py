import functools
import jwt
import boto3
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Response, json
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from flaskr.db import get_db
from .sms import Autoemail
from itsdangerous import URLSafeTimedSerializer
from flask_cors import cross_origin

from google.oauth2 import id_token
from google.auth.transport import requests as requestgoogle


bp = Blueprint('auth', __name__, url_prefix='/auth')
ts = URLSafeTimedSerializer("dev")

@bp.route('/register', methods=('GET', 'POST'))
@cross_origin()
def register():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['pw']
        if (not email or not password) :
            return jsonify(body = "Email or password is incorrect", code = 0)

        db = get_db()
        error = None

        if not email:
            error = 'email is required.'
            return jsonify(body=error, code = 0)
        elif not password:
            error = 'Password is required.'
            return jsonify(body=error, code = 0)
        elif db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'User: {} is already registered.'.format(email)
            return jsonify(body=error, code = 0)

        if error is None:
            db.execute(
                'INSERT INTO user (email, password, status) VALUES (?, ?, 0)',
                (email, generate_password_hash(password))
            )
            db.commit()
            sns = boto3.resource('sns', region_name='us-east-2')
            topic = sns.Topic('arn:aws:sns:us-east-2:064845973938:ElasticBeanstalkNotifications-Environment-6156-env')
            response = topic.publish(
                Message='send email',
                Subject='new register',
                MessageAttributes={
                    "email": {
                        'DataType': 'String',
                        "StringValue": email
                    }
                }
            )
        # return jsonify(body=str(response), code = 1)
        return jsonify(body="An email will be sent to you!", code=1)


@bp.route('/google', methods=('GET', 'POST'))
@cross_origin()
def google():
    CLIENT_ID = "1076764154881-jq0lgjdbeje9b5tsucimo3l8p48uen0v.apps.googleusercontent.com"
    token = request.form['idtoken']
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requestgoogle.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        email = idinfo['email']
        password = "googlezw2497"
        '''
        check if it exist this email
        '''
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if not user:
            db.execute(
                'INSERT INTO user (email, password, status) VALUES (?, ?, ?)',
                (email, generate_password_hash(password), 1)
            )
            db.commit()

        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        try:
            payload = {
                        'user_id': user['id'],
                        'email': user['email']
                        }
            token = jwt.encode(payload, 'dev', algorithm='HS256')
        except Exception as e:
            return jsonify(status = 401, msg = "invalid", code = 0)
        else:
            data =  {'authorization': "{}".format(token.decode()),"status" : 1, "code" : 1}
            js = json.dumps(data)
            resp = Response(js, status=200, mimetype='application/json')
            return resp

    except ValueError:
        # Invalid token
        jsonify(status=401, msg="invalid", code=0)


@bp.route('/login', methods=('GET', 'POST'))
@cross_origin()
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['pw']
        if (not email or not password) :
            return jsonify(body = "Email or password is incorrect", code = 0)
        db = get_db()
        user = db.execute(
                     'SELECT * FROM user WHERE email = ?', (email,)
                 ).fetchone()
        if user is None:
            return jsonify(body = "Email or password is incorrect", code = 0)

        if (not check_password_hash(user['password'], password)) :
            return jsonify(body="Email or password is incorrect", code = 0)

        try:
            payload = {
                        'user_id': user['id'],
                        'email': user['email']
                        }
            token = jwt.encode(payload, 'dev', algorithm='HS256')
        except Exception as e:
            return jsonify(status = 401, msg = "invalid", code = 0)
        else:
            data =  {'authorization': "{}".format(token.decode()), "confirm" : user['status'], "code" : 1}
            js = json.dumps(data)
            resp = Response(js, status=200, mimetype='application/json')
            return resp

@bp.route('/confirm')
def confirm_email():
    token = request.args.get("context")
    try:
        payload = jwt.decode(token, 'dev', algorithms='HS256')
        email = payload['email']
    except:
        abort(404)
    db = get_db()
    id = db.execute(
        'SELECT id FROM user WHERE email = ?', (email,)
    ).fetchone()
    if id is not None:
        db.execute(
            'UPDATE user SET status = 1 WHERE email = ?',(email,)
        )
    else:
        abort(403)
    db.commit()

    return jsonify(msg="email confirmation success", code=1)


@bp.route('/oauth2callback.html')
def oauth2callback():
    return render_template('auth/oauth2callback.html')

@bp.route('/admin')
def admin():
    db = get_db()
    ss = ' '
    profile = db.execute('SELECT * FROM user').fetchall()
    for n in range(len(profile)):
        ss += "<p>Email: [%s]  Confirm: [%s] Password: [%s] </p>" % (profile[n]['email'], 'True' if profile[n]['status'] == 1 else 'False', profile[n]['password'])
        #ss += profile[n]['email'] + '   Status:' + str(profile[n]['status']) + '   Password:' + profile[n]['password'] + '\n' + '\n'
    return ss


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view















