from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,json,jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, email, status'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    print(type(posts))
    p = {}
    for i,j in enumerate(posts):
        p[i] = j['body']
    return jsonify(posts = p)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
            return jsonify(error=error, code = 0)

        db = get_db()
        db.execute(
            'INSERT INTO post (title, body, author_id)'
            ' VALUES (?, ?, ?)',
            (title, body, g.user['id'])
        )
        db.commit()
        return jsonify(body="success", code = 0)

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    admin = 1
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, email'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if g.user['id'] == admin:
        return post

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/profile')
@login_required
def profile(id):
    db = get_db()
    profile = db.execute('SELECT * FROM profile AS P WHERE user_id = ?', (id,)).fetchone()
    return render_template('blog/profile.html', profile=profile)


@bp.route('/<int:id>/profileupdate', methods=('GET', 'POST'))
@login_required
def profileupdate(id):
    if request.method == 'POST':
        email = request.form['email']
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        description = request.form['description']
        error = None
        if not email:
            error = 'Email is required.'
        if not lastname:
            error = 'Lastname is required.'
        if not firstname:
            error = 'Firstname is required.'
        if not description:
            error = 'Description is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            profile = db.execute('SELECT * FROM profile AS P WHERE user_id = ?', (id,)).fetchone()
            if not profile :
                db.execute(
                    'INSERT INTO profile (user_id, email, description, firstname, lastname)'
                    ' VALUES (?, ?, ?, ?, ?)',
                    (g.user['id'], email, description, firstname, lastname)
                )
            else:
                db.execute(
                    'UPDATE profile SET email=?, description=?, firstname=?, lastname=?'
                    ' WHERE id=?',
                    (email, description, firstname, lastname, id)
                )
            db.commit()
            return redirect(url_for('blog.profile', id =g.user['id'] ))
    return render_template('blog/profileupdate.html')

