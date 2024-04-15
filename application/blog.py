from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from application.auth import login_required
from application import db
from application.lib import request_input
from application.model import Post
from application.model import User

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = Post.query.with_entities(
        Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username
    ).join(User).order_by(Post.created.desc()).all()

    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':

        data = {
            "title": request_input("title"), 
            "body": request_input("body"), 
            "author_id": g.user.id
        }
        
        error = None

        if not data.get("title"):
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(**data)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
        
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    
    post = db.session.query(
        Post.id, Post.title, Post.body, Post.created, Post.author_id, User.username
    ).join(User).filter(Post.id == id).first()
    
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        
        data = {
            "title": request_input("title"), 
            "body": request_input("body"), 
        }
        
        error = None

        if not data.get("title"):
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post.query.filter_by(id=id).first()
            post.title = data.get("title")
            post.body = data.get("body")
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))