# backend/app/__init__.py

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


#from app.Tokens.model import Token

db = SQLAlchemy()
app = None

login_manager = LoginManager()
UPLOAD_FOLDER = '/home/bihut/uploadFolder/'
SECRET_KEY = "o;A3#sEt&lT_6vYmC!M8c~*IW,TQYdGCk]Yrob|g-T6fbzQLqudrXSfI}vu'6;4"
def create_app():
    global app
    global jwt
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://caleta:Caleta123456=@localhost:3306/caleta'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['JWT_SECRET_KEY'] = 'a6fVBPyGVAM2PerbAzwP85dmZwxz0ODU'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    login_manager.init_app(app)
    db.init_app(app)
    # Registro de los Blueprints
    # blueprint for auth routes in our app
    from .api.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .public import public_bp
    app.register_blueprint(public_bp)
    from .api import API_bp
    app.register_blueprint(API_bp)
    from .user.model import User

    from .Tokens.model import  Token

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.get_by_id(int(user_id))

    with app.app_context():
        db.create_all()
        db.session.commit()
        #jwt = JWTManager(app)
        print("db created")
        if Token.get_by_username("dani") == None:
            Token.initTokens()
        #Token.initTokens()
    return app
