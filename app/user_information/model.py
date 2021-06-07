from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User_Information(db.Model):

    __tablename__ = 'user_information'

    iduser = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(45))
    lastname = db.Column(db.String(45))
    birthdate = db.Column(db.TIMESTAMP)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(15))
    city = db.Column(db.String(45))
    comments = db.Column(db.String(200))
    photo = db.Column(db.String(200))
    #email = db.Column(db.String(45), nullable=False)

    def __init__(self, iduser,name,lastname,birthdate,address,phone,city,comments, photo):
        self.iduser = iduser
        self.name = name
        self.lastname = lastname
        self.birthdate = birthdate
        self.address = address
        self.phone = phone
        self.city = city
        self.comments = comments
        self.photo = photo
        #self.email = email
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
        return User_Information.query.get(id)



    @staticmethod
    def print(id):
        return User_Information.query.get(id)