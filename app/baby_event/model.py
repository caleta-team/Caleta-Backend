
import time
from flask_login import UserMixin

from app import db
from app.utils.utils import Utils


class BabyEvent(db.Model):

    __tablename__ = 'baby_event'

    idbaby = db.Column(db.BIGINT,unique=True,primary_key=True)
    idevent = db.Column(db.BIGINT,unique=True,primary_key=True)


    def __init__(self, idbaby, idevent):
        self.idbaby = idbaby
        self.idevent = idevent
        # datetime.now()

    def getJSON(self):
        return {
            'idevent': self.idevent,
            'idbaby': self.idbaby

        }

    def __repr__(self):
        return f'<event {self.idevent}>'
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

    @staticmethod
    def get_by_babyid(id):
        return db.session.query(BabyEvent).filter(BabyEvent.idbaby == id).all()
        #return  BabyEvent.query.get(id)


    @staticmethod
    def print(id):
        return BabyEvent.query.get(id)

    @staticmethod
    def getAllEventsJSON():
        events=BabyEvent.query.all()
        data_set = []
        i=0
        for event in events:
            aux=event.getJSON()
            data_set.append(aux)
            i=i+1
        return data_set