from flask import abort, render_template
from flask import request
from . import public_bp
from ..Tokens.model import Token
from ..baby.model import Baby
from ..user.model import User


@public_bp.route('/username/<string:username>',methods=['GET'])
def getUsername(username):
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:
        user=User.get_by_username(username)
        return {'payload': user.getJSON()}, 200

@public_bp.route('/username',methods=['POST'])
def createNewUsername():
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:
        try:
            data = request.get_json()
            if data == None:
                return {'message': 'No data available'}, 401
            else:
                #type = Utils.getTypeMD(), email = None, username = None, password = None, name = "", lastname = "", photo = ""
                user = User(data['type'],data['email'],data['username'],data['password'],data['name'],data['lastname'],data['photo'])
                res=user.save()

                if res == True:
                    return {"success":'User created!'}, 200
                else:
                    return {'message': 'Error creating user'}, 401
        except:
           return {'message': 'Error creating user (data missed or already registered)'}, 401

@public_bp.route('/baby/<int:babyid>',methods=['GET'])
def getBaby(babyid):
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:
        baby=Baby.get_by_id(babyid)
        return {'payload': baby.getJSON()}, 200

@public_bp.route('/baby',methods=['POST'])
def createNewBaby():
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:
        try:
            data = request.get_json()
            if data == None:
                return {'message': 'No data available'}, 401
            else:
                #type = Utils.getTypeMD(), email = None, username = None, password = None, name = "", lastname = "", photo = ""
                #user = User(data['type'],data['email'],data['username'],data['password'],data['name'],data['lastname'],data['photo'])
                #res=user.save()
                baby = Baby(data['name'],data['lastname'],data['photo'])
                res = baby.save()
                if res == True:
                    return {"success":'Baby created!'}, 200
                else:
                    return {'message': 'Error creating user'}, 401
        except:
           return {'message': 'Error creating user (data missed or already registered)'}, 401
'''
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
'''