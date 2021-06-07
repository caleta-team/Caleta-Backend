from flask import Blueprint, Flask, render_template, flash, redirect, request, session, logging, url_for, jsonify
from flask_restful import reqparse
from werkzeug.security import generate_password_hash, check_password_hash


from ..user.model import User
from ..user_information.model import User_Information
from app import db
from ..utils.utils import *

from ..Tokens.model import RevokedTokenModel
'''
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
'''
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import pdb

auth = Blueprint('auth', __name__)
parser = reqparse.RequestParser()
parser.add_argument('username', help='username cannot be blank', required=True)
parser.add_argument('password', help='password cannot be blank', required=True)
parser.add_argument('email', help='email cannot be blank', required=False)
parser.add_argument('type', help='type cannot be blank', required=False)

'''
@auth.route('/signupjwt', methods=['POST'])
def singupjwt():
    data = request.get_json()


    #new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    new_user = User(type=type, email=data['email'],

                    username=data['username'],

                    password=User.generate_hash( generate_password_hash(data['password'], method='sha256'))

                    )
    new_user.save()
    db.session.commit()
    ##db.session.add(new_user)
    ##db.session.commit()
    return jsonify({'message': 'registered successfully'})

    ###--------------otra versión
    data = parser.parse_args()
    username = data['username']
    email = data['email']
    type = data['type']
    password = data['password']
    # Checking that user is already exist or not
    if User.get_by_username(username) or User.get_by_email(email):
        return {'message': f'User {username} already exists'}
    #new_user = User(request.form.get('type'), email=email, username=username, password=generate_password_hash(password, method='sha256'), jwt=-1)

    # create new user
    new_user = User(type=type, email=email,

        username=username,

        password=User.generate_hash(password)

    )

    try:

        # Saving user in DB and Generating Access and Refresh token
        new_user.save()

        access_token = create_access_token(identity=username)

        refresh_token = create_refresh_token(identity=username)

        return {

            'message': f'User {username} was created',

            'access_token': access_token,

            'refresh_token': refresh_token

        }

    except:

        return {'message': 'Something went wrong'}, 500

'''

@auth.route('/loginjwt', methods=['POST'])
def loginjwt():
    data = parser.parse_args()

    username = data['username']
    password = data['password']

    # Searching user by username
    if Utils.checkEmail(username):
        current_user = User.get_by_email(username)
    else:
        current_user = User.get_by_username(username)

    # user does not exists
    if not current_user:
        return {'message': f'User {username} doesn\'t exist'}


    print(current_user.username)
    print(password)
    print(current_user.password)
    # user does not exists
    #if not current_user:
     #   return {'message': f'User {username} doesn\'t exist'}
    # user exists, comparing password and hash
    #password = User.generate_hash(password)
    #print(password)
    if User.verify_hash(password, current_user.password):
        # generating access token and refresh token
        access_token = create_access_token(identity=username)

        refresh_token = create_refresh_token(identity=username)

        return {
            'message': f'Logged in as {username}',
            'access_token': access_token,
            'refresh_token': refresh_token

        }

    else:

        return {'message': "Wrong credentials"}





@auth.route('/login', methods=['POST'])
def login():
    # checking that user is exist or not by email
    identifier = request.form.get('identifier')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.get_by_email(identifier)
    userbyusername = User.get_by_username(identifier)
    if user is None:
        user = userbyusername

    #user = User.query.filter_by(email=identifier).first()
    print("TYPE")
    print(user.password)
    if user:
        if check_password_hash(user.password, password):
            # if password is matched, allow user to access and save email and username inside the session
            flash('You have successfully logged in.', "success")
            session['logged_in'] = True
            session['email'] = user.email
            session['username'] = user.username
            # After successful login, redirecting to home page
            return "logeado correctamente"
        else:
            # if password is in correct , redirect to login page
            flash('Username or Password Incorrect', "Danger")
            return "incorrecto"
    # rendering login page
    return "incorrecto"

@auth.route('/signup',methods=['POST'])
def signup():
    data = parser.parse_args()
    email =  data['email']
    username =  data['username']
    password = data['password']
    #user = User.get_by_email(email)  # if this returns a user, then the email already exists in database

    if User.get_by_email(email) or User.get_by_username(username):  # if a user is found, we want to redirect back to signup page so user can try again
        return "ya existe"

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    password_aux = generate_password_hash(password)
    print("password_aux")
    print(password_aux)
    type = Utils.getTypeUser()
    if(data['type'] is not None):
        type = request.form.get("type")

    new_user = User(type=type, email=email, username=username, password=password_aux, jwt=-1)
    # add the new user to the database
    #db.session.add(new_user)
    #db.session.commit()
    new_user.save()
    try:
        user = User.get_by_email(email)

        user_information = User_Information(user.iduser, request.form.get('name'), request.form.get('lastname'),
                                            request.form.get('birthdate'), request.form.get('address'), request.form.get('phone'),
                                            request.form.get('city'), request.form.get('comments'), request.form.get('photo'))
        #db.session.add(user_information)
        user_information.save()
    except:
        print("e")
    #return redirect(url_for('auth.login'))
    db.session.add(new_user)
    db.session.commit()
    flash('You have successfully registered', 'success')
    return {'message': 'registrado correctamente'},200
@auth.route('/logout')
def logout():
    #session['logged_in'] = False
    #return 'Logout'
    jti = get_jwt()['jti']

    try:
        # Revoking access token
        revoked_token = RevokedTokenModel(jti=jti)

        revoked_token.add()

        return {'message': 'Access token has been revoked'}

    except:

        return {'message': 'Something went wrong'}, 500


@auth.route('/logout/refresh')
def logoutrefresh():
    jti = get_jwt()['jti']

    try:

        revoked_token = RevokedTokenModel(jti=jti)

        revoked_token.add()

        pdb.set_trace()

        return {'message': 'Refresh token has been revoked'}

    except:

        return {'message': 'Something went wrong'}, 500


@auth.route('/token/refresh')
def tokenrefresh():
    current_user = get_jwt_identity()

    access_token = create_access_token(identity=current_user)

    return {'access_token': access_token}
