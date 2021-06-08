from app import db


class Token(db.Model):
    __tablename__ = 'tokens'

    username = db.Column(db.String(20), primary_key=True)
    token = db.Column(db.String(20))
    time = db.Column(db.BIGINT)
    def __init__(self, username, token,time):
        self.username = username
        self.token = token
        self.time = time




    @staticmethod
    def initTokens():
        from datetime import datetime
        now = datetime.now()
        timestamp = datetime.timestamp(now)

        t = Token("dani","5JheYOkq1GpRuPxqb9qq",timestamp)
        t.save()

        t = Token("angel","Z9893PvQrHTHkLOgLI4T",timestamp);
        t.save()

        t = Token("david", "BubKw7Cd7G0JyHENXQVO", timestamp);
        t.save()

        t = Token("lionel", "Ln3uuNWkW65upPnJIkfp", timestamp);
        t.save()

        t = Token("leopoldo", "MXuBnE7wcVDrE67Ejga1", timestamp);
        t.save()

        t = Token("blas", "WGVutzn9zyFRXXvK23Xu", timestamp);
        t.save()

        t = Token("andres", "F9qkMQ1151Xn7k7Q5CR3", timestamp);
        t.save()

    """
    Save Token in DB
    """
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_username(username):
        return Token.query.filter_by(username=username).first()

    @staticmethod
    def checkAuthorization(token):
        aux = Token.query.filter_by(token=token).first()
        if aux==None:
            return False
        else:
            return aux