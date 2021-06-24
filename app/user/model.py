from datetime import datetime


import time
from flask_login import UserMixin

from app import db
from ..utils.utils import Utils

class User(db.Model, UserMixin):

    __tablename__ = 'user'


    email = db.Column(db.String(45), unique=True, nullable=False)
    username = db.Column(db.String(45), unique=True, nullable=False,primary_key=True)
    password = db.Column(db.String(45), nullable=False)
    type = db.Column(db.SMALLINT,nullable=False,default=Utils.getTypeMD())
    photo=db.Column(db.String(200))
    name=db.Column(db.String(45))
    lastname = db.Column(db.String(45))
    create_time = db.Column(db.BIGINT)

    def __init__(self, type=Utils.getTypeMD(), email=None, username=None, password=None, name="", lastname="",photo=""):
        self.type = type
        self.email = email
        self.username = username
        self.password = password
        self.name = name
        self.lastname = lastname
        self.photo = photo
       # self.password = sha256.hash(password)

        self.create_time = int(round(time.time() * 1000))
        # datetime.now()


    def __repr__(self):
        return f'<User {self.iduser}>'
    '''
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

    '''
    #def set_password(self, password):
    #    self.password = generate_password_hash(password)

    #def check_password(self, password):
    #    return check_password_hash(self.password, password)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def getJSON(self):
        return {
            'username': self.username,
            'name': self.name,
            "lastname":self.lastname,
            "type":self.type,
            "photo":self.photo

        }
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

