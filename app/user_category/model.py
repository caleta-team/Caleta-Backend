from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User_Category(db.Model):

    __tablename__ = 'user_category'

    iduser = db.Column(db.BIGINT, primary_key=True)
    #email = db.Column(db.String(100), unique=True)
    #password = db.Column(db.String(100))
    #name = db.Column(db.String(1000))
    name = db.Column(db.String(30))

    def __init__(self, name):
        self.name = name
        #self.password = bcrypt.generate_password_hash(
        #    password, app.config.get('BCRYPT_LOG_ROUNDS')
        #).decode()


    def __repr__(self):
        return f'<User {self.iduser}>'

    #def set_password(self, password):
    #    self.password = generate_password_hash(password)

    #def check_password(self, password):
    #    return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)

    @staticmethod
    def get_by_id(id):
        return User_Category.query.get(id)

    #@staticmethod
    #def get_by_email(email):
    #    return User.query.filter_by(email=email).first()

    @staticmethod
    def print(id):
        return User_Category.query.get(id)