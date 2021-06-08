from flask import abort, render_template
from flask import request
from . import public_bp
from ..Tokens.model import Token


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
        aux=Token.checkAuthorization(request.headers['token'])
        if aux==None:
            return {'message': 'Non Authorised - Not valid token'}, 401
        else:
            return {'message': 'Authorised:'+str(aux.username)}, 200
    else:
        return {'message': 'Non Authorised - Token missed'},401
