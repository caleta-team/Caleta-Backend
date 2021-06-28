
import time
from flask_login import UserMixin

from app import db
from app.utils.utils import Utils


class Event(db.Model, UserMixin):

    __tablename__ = 'event'

    idevent = db.Column(db.BIGINT,unique=True,primary_key=True)
    type = db.Column(db.String(10),default=Utils.getTypeActivity())
    comments = db.Column(db.String(45))
    anomaly = db.Column(db.BOOLEAN,default=False)
    name = db.Column(db.String(45))
    create_time = db.Column(db.BIGINT)

    def __init__(self, name="",type=Utils.getTypeActivity(),comments="",anomaly=False):
        self.name = name
        self.type = type
        self.comments = comments
        self.anomaly = anomaly
        self.create_time = int(round(time.time() * 1000))
        # datetime.now()

    def getJSON(self):
        return {
            'idevent': self.idevent,
            'type': self.type,
            "comments": self.comments,
            "time":self.create_time,
            "anomaly": self.anomaly,
            "name":self.name

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
            db.session.flush()
            return True
        except:
            return False

    @staticmethod
    def get_by_id(id):
        return Event.query.get(id)


    @staticmethod
    def print(id):
        return Event.query.get(id)

    @staticmethod
    def getAllEventsJSON():
        events=Event.query.all()
        data_set = []
        i=0
        for event in events:
            aux=event.getJSON()
            data_set.append(aux)
            i=i+1
        return data_set