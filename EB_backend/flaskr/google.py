from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_dance.contrib.google import make_google_blueprint, google
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = make_google_blueprint(
    client_id="129231482545-2svae7d41m112685j7b53u388tu5kk9t.apps.googleusercontent.com",
    client_secret="YbbS3Ebtb1CVybyu-Fu7d1YH",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ],
    redirect_to="google.googlelogin"
)


@bp.route("/googlelogin")
def googlelogin():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    email = resp.json()["email"]
    password = "google"
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
    session.clear()
    session['user_id'] = user['id']
    session['status'] = user['status']
    profile = db.execute('SELECT * FROM user').fetchall()
    return redirect(url_for('blog.index'))