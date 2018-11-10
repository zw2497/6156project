import functools
import jwt
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Response, json
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from flaskr.db import get_db
from .sms import Autoemail
from itsdangerous import URLSafeTimedSerializer
from flask_cors import cross_origin


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
        return jsonify(body="Register success", code = 1)



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
                        'email': user['email'],
                        'status': user['status']
                        }
            token = jwt.encode(payload, 'dev', algorithm='HS256')
        except Exception as e:
            return jsonify(status = 401, msg = "invalid", code = 0)
        else:
            data =  {'authorization': "{}".format(token.decode()), "code" : 1}
            js = json.dumps(data)
            resp = Response(js, status=200, mimetype='application/json')
            # resp.headers['qwert'] = token
            return resp

@bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="dev", max_age=86400)
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

    return redirect(url_for('blog.index'))


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















