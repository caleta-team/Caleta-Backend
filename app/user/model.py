from datetime import datetime

import bcrypt
from passlib.hash import pbkdf2_sha256 as sha256
import time
from flask_login import UserMixin
from functools import wraps
from flask import Flask, request, jsonify, make_response
import jwt

from werkzeug.security import generate_password_hash, check_password_hash

import app
from app import db
from ..utils.utils import Utils

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    iduser = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    jwt = db.Column(db.String(50))
    create_time = db.Column(db.BIGINT)
    type = db.Column(db.SMALLINT, default=Utils.getTypeUser())
    def __init__(self, type=Utils.getTypeUser(), email=None, username=None, password=None, jwt=-1):
        self.type = type
        self.email = email
        self.username = username
        self.password = password
        self.jwt = jwt
       # self.password = sha256.hash(password)

        self.create_time = int(round(time.time() * 1000))
        # datetime.now()


    def __repr__(self):
        return f'<User {self.iduser}>'

    @classmethod
    def return_all(cls):

        def to_json(x):
            return {

                'username': x.username,
                'password': x.password

            }

        return {'users': [to_json(user) for user in User.query.all()]}

    """
    Delete user data
    """

    @classmethod
    def delete_all(cls):

        try:

            num_rows_deleted = db.session.query(cls).delete()

            db.session.commit()

            return {'message': f'{num_rows_deleted} row(s) deleted'}

        except:

            return {'message': 'Something went wrong'}

    """
    generate hash from password by encryption using sha256
    """

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    """
    Verify hash and password
    """

    @staticmethod
    def verify_hash(password, hash_):
        return sha256.verify(password, hash_)


    #def set_password(self, password):
    #    self.password = generate_password_hash(password)

    #def check_password(self, password):
    #    return check_password_hash(self.password, password)

    def save(self):
        if not self.iduser:
            db.session.add(self)
            #db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def print(id):
        return User.query.get(id)

    def token_required(f):
        @wraps(f)
        def decorator(*args, **kwargs):

            token = None

            if 'x-access-tokens' in request.headers:
                token = request.headers['x-access-tokens']

            if not token:
                return jsonify({'message': 'a valid token is missing'})

            try:
                data = jwt.decode(token, app.config[app.SECRET_KEY])
                current_user = User.query.filter_by(id=data['id']).first()
            except:
                return jsonify({'message': 'token is invalid'})

            return f(current_user, *args, **kwargs)

        return decorator