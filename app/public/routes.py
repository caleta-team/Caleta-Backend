from flask import abort, render_template
from flask import request
from . import public_bp
from ..Tokens.model import Token
from ..baby.model import Baby
from ..event.model import Event
from ..user.model import User
from flask import Flask, render_template, Response
import cv2
import depthai as dai

@public_bp.route('/username/<string:username>',methods=['GET'])
def getUsername(username):
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:
        user=User.get_by_username(username)
        return {'payload': user.getJSON()}, 200

@public_bp.route('/username',methods=['POST'])
def createNewUsername():
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:
        try:
            data = request.get_json()
            if data == None:
                return {'message': 'No data available'}, 401
            else:
                #type = Utils.getTypeMD(), email = None, username = None, password = None, name = "", lastname = "", photo = ""
                user = User(data['type'],data['email'],data['username'],data['password'],data['name'],data['lastname'],data['photo'])
                res=user.save()

                if res == True:
                    return {"success":'User created!'}, 200
                else:
                    return {'message': 'Error creating user'}, 401
        except:
           return {'message': 'Error creating user (data missed or already registered)'}, 401

@public_bp.route('/baby/<int:babyid>',methods=['GET'])
def getBaby(babyid):
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:
        baby=Baby.get_by_id(babyid)
        return {'payload': baby.getJSON()}, 200

@public_bp.route('/baby',methods=['POST'])
def createNewBaby():
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:
        try:

            data = request.get_json()
            #print(data)
            if data == None:
                return {'message': 'No data available'}, 401
            else:
                #type = Utils.getTypeMD(), email = None, username = None, password = None, name = "", lastname = "", photo = ""
                #user = User(data['type'],data['email'],data['username'],data['password'],data['name'],data['lastname'],data['photo'])
                #res=user.save()
                baby = Baby(data['name'],data['lastname'],data['photo'])
                res = baby.save()
                if res == True:
                    return {"success":'Baby created!'}, 200
                else:
                    return {'message': 'Error creating user'}, 401
        except:
           return {'message': 'Error creating baby (data missed or already registered)'}, 401


@public_bp.route('/baby',methods=['GET'])
def listBabies():
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:

        #//event=Event.get_by_id(eventid)
        allbabies = Baby.getAllBabyJSON()
        return {'payload': allbabies}, 200


@public_bp.route('/event',methods=['GET'])
def listEvents():
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:

        #//event=Event.get_by_id(eventid)
        allevents = Event.getAllEventsJSON()

        return {'payload': allevents}, 200

@public_bp.route('/event/<int:eventid>',methods=['GET'])
def getEvent(eventid):
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:
        event=Event.get_by_id(eventid)
        return {'payload': event.getJSON()}, 200

@public_bp.route('/event',methods=['POST'])
def createNewEvent():
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:
        try:
            data = request.get_json()
            if data == None:
                return {'message': 'No data available'}, 401
            else:
                #type = Utils.getTypeMD(), email = None, username = None, password = None, name = "", lastname = "", photo = ""
                #user = User(data['type'],data['email'],data['username'],data['password'],data['name'],data['lastname'],data['photo'])
                #res=user.save()
                #print(str(data['anomaly']) +"   "+str(type(data['anomaly'])))
                event = Event(data['name'],data['type'],data['comments'],data['anomaly'])
                res = event.save()
                if res == True:
                    return {"success":'Event created!'}, 200
                else:
                    return {'message': 'Error creating event'}, 401
        except:
           return {'message': 'Error creating event (data missed or already registered)'}, 401


def gen_frames():  # generate frame by frame from camera
    while True:
        # Create pipeline
        pipeline = dai.Pipeline()

        # Define source and output
        camRgb = pipeline.createColorCamera()
        xoutVideo = pipeline.createXLinkOut()

        xoutVideo.setStreamName("video")

        # Properties
        camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        camRgb.setVideoSize(1280, 720)
        ve2 = pipeline.createVideoEncoder()
        ve2.setDefaultProfilePreset(1280, 720, 30, dai.VideoEncoderProperties.Profile.MJPEG)
        camRgb.video.link(ve2.input)

        #camRgb.setVideoSize(640,400)

        xoutVideo.input.setBlocking(False)
        xoutVideo.input.setQueueSize(1)

        # Linking
        camRgb.video.link(xoutVideo.input)
        # Connect to device and start pipeline
        qRgb = None
        inRgb = None
        frame = None
        with dai.Device(pipeline) as device:
            # Output queue will be used to get the rgb frames from the output defined above
            qRgb = device.getOutputQueue(name="video", maxSize=1, blocking=False)

            while True:
                inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived
                frame = inRgb.getCvFrame() # read the camera frame

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@public_bp.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@public_bp.route('/oak')
def index():
    """Video streaming home page."""
    return render_template('index.html')


'''
@public_bp.route('/')
def index():
    return render_template('index.html')

@public_bp.route('/profile')
def profile():
    return render_template('profile.html')

@public_bp.route('/login', methods=['GET'])
def login_web():
    return render_template('login.html')

@public_bp.route('/signup', methods=['GET'])
def signup_web():
    return render_template('signup.html')

@public_bp.route("/p/<string:slug>/")
def show_post(slug):
    #post = Post.get_by_slug(slug)
    #if post is None:
    #    abort(404)
    #return render_template("public/post_view.html", post=post)
    if 'token' in request.headers:
        aux=Token.checkAuthorization(request.headers['token'])
        if aux==None:
            return {'message': 'Non Authorised - Not valid token'}, 401
        else:
            return {'message': 'Authorised:'+str(aux.username)}, 200
    else:
        return {'message': 'Non Authorised - Token missed'},401
'''