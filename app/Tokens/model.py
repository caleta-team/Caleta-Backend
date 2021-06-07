from app import db


class Token(db.Model):
    __tablename__ = 'tokens'

    username = db.Column(db.String(120), primary_key=True)
    token = db.Column(db.String(120))
    time = db.Column(db.BIGINT)
    def __init__(self, username, token,time):
        self.username = username
        self.token = token
        self.time = time

    """
    Save Token in DB
    """
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_username(username):
        return Token.query.filter_by(username=username).first()