from flask import abort, render_template
from flask import request
from . import public_bp
@public_bp.route('/')
def index():
    return render_template('index.html')

@public_bp.route('/profile')
def profile():
    return render_template('profile.html')

@public_bp.route('/login', methods=['GET'])
def login_web():
    return render_template('login.html')

@public_bp.route('/signup', methods=['GET'])
def signup_web():
    return render_template('signup.html')

@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    #post = Post.get_by_slug(slug)
    #if post is None:
    #    abort(404)
    #return render_template("public/post_view.html", post=post)
    if 'token' in request.headers:
        return request.headers['token']
    else:
        return {'message': 'Non Authorised'},401

    #return 'Hello World2!'