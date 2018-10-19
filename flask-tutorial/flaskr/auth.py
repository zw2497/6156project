import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from flaskr.db import get_db

from .sms import Autoemail

from itsdangerous import URLSafeTimedSerializer


bp = Blueprint('auth', __name__, url_prefix='/auth')

ts = URLSafeTimedSerializer("dev")

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'email is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO user (email, password, status) VALUES (?, ?, 0)',
                (email, generate_password_hash(password))
            )
            db.commit()

            # Now we'll send the email confirmation link
            subject = "Hello World"
            token = ts.dumps(email, salt='dev')
            confirm_url = url_for(
                'auth.confirm_email',
                token=token,
                _external=True)
            #html = "Your account confirmation link is: %s"
            html = "hello world: %s" % (confirm_url)
            confirmation = Autoemail(email, subject, html)
            confirmation.send()



            return redirect(url_for('auth.login'))
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['status'] = user['status']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    status = session.get('status')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()



@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))


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















