from flask import abort, render_template
#from app.models import Post
from . import API_bp
from app import db
from app.user.model import User
from flask import Flask, send_from_directory, flash, request, redirect, url_for, session
from app import app
import os

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webm'}
from werkzeug.utils import secure_filename

__tablename__ = 'test'
idtest = db.Column(db.Integer, primary_key=True)
data1 = db.Column(db.String(80), nullable=False)
data2 = db.Column(db.String(80), nullable=False)
@API_bp.route('/api/ap1/<int:post_idexample>/')
def func1(post_idexample):
    user = User.get_by_id(post_idexample)
    return user.data1 + user.data2

@API_bp.route('/api/ap2')
def func2():
    if (session is not None and session.get("username") and session["username"] is not None):
        return "ha accedido "+session["username"]
    else:
        #print(session["username"])
        return "no hay nadie logeado"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@API_bp.route('/login',methods=['POST'])
def login_user():
    return ""

@API_bp.route('/api/file/',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file',
             #                       filename=filename))
    return ""

@app.route('/uploads/<filename>')
def uploaded_file(filename):
   return send_from_directory(app.config['UPLOAD_FOLDER'],filename)