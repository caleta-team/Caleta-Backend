
import time

from app import db


class Baby(db.Model):

    __tablename__ = 'baby'

    idbaby = db.Column(db.BIGINT,unique=True,primary_key=True)
    photo=db.Column(db.String(200))
    name=db.Column(db.String(45))
    lastname = db.Column(db.String(45))
    create_time = db.Column(db.BIGINT)

    def __init__(self, name="", lastname="",photo=""):
        self.type = type
        self.name = name
        self.lastname = lastname
        self.photo = photo
       # self.password = sha256.hash(password)

        self.create_time = int(round(time.time() * 1000))
        # datetime.now()

    def getJSON(self):
        return {
            'idbaby': self.idbaby,
            'name': self.name,
            "lastname": self.lastname,

            "photo": self.photo

        }

    def __repr__(self):
        return f'<User {self.idbaby}>'
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
    def get_by_id(id):
        return Baby.query.get(id)


    @staticmethod
    def print(id):
        return Baby.query.get(id)

    @staticmethod
    def getAllBabyJSON():
        babies=Baby.query.all()
        data_set = []
        i=0
        for baby in babies:
            aux=baby.getJSON()
            data_set.append(aux)
            i=i+1
        return data_set
