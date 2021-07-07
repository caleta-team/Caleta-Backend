# backend/app/__init__.py

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .utils.mqtt import MQTTCaleta

#from app.Tokens.model import Token


db = SQLAlchemy()
app = None
mqtt=None
login_manager = LoginManager()
UPLOAD_FOLDER = '/home/bihut/uploadFolder/'
SECRET_KEY = "o;A3#sEt&lT_6vYmC!M8c~*IW,TQYdGCk]Yrob|g-T6fbzQLqudrXSfI}vu'6;4"
def create_app():
    global app,mqtt
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

#cnx = mysql.connector.connect(user="caleta@caleta", password={your_password}, host="caleta.mysql.database.azure.com", port=3306, database={your_database}, ssl_ca={ca-cert filename}, ssl_verify_cert=true)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://caleta@caleta:&T\qhruU3Q[h5Zh2@caleta.mysql.database.azure.com:3306/caleta'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    #app.config['JWT_SECRET_KEY'] = 'a6fVBPyGVAM2PerbAzwP85dmZwxz0ODU'
    #app.config['JWT_BLACKLIST_ENABLED'] = True
    #app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    login_manager.init_app(app)
    db.init_app(app)

    # Registro de los Blueprints
    # blueprint for auth routes in our app

    from .public import public_bp
    app.register_blueprint(public_bp)

    from .api import API_bp
    app.register_blueprint(API_bp)

    #from .user.model import User
    #app.register_blueprint(User)

    from .Tokens.model import  Token
    #app.register_blueprint(Token)

    from .event.model import Event
    #app.register_blueprint(Event)

    from .baby.model import Baby
    #app.register_blueprint(Baby)
    from .baby_event.model import BabyEvent

    from .event_activity.model import EventActivity
    from .event_respiration.model import EventRespiration
    from .event_stress.model import EventStress
    #@login_manager.user_loader
    #def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
    #    return User.get_by_id(int(user_id))


    #mqtt
    #mqtt = MQTTCaleta("client1")
    with app.app_context():
        db.create_all()
        db.session.commit()
        #jwt = JWTManager(app)
        print("db created")
        if Token.get_by_username("dani") == None:
            Token.initTokens()
        #Token.initTokens()

    return app

def on_subscribe(client, userdata, mid, granted_qos):
    print('Subscribed for m' + str(mid))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))

def on_log(client, userdata, level, buf):
    print("log: ",buf)