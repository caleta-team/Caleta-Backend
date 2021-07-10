import subprocess

from . import public_bp
from ..Tokens.model import Token
from ..baby.model import Baby
from ..event.model import Event
from ..event_activity.model import EventActivity
from ..event_respiration.model import EventRespiration
from ..event_stress.model import EventStress
from ..user.model import User
from flask import render_template, Response, request
import cv2
import depthai as dai
import traceback
from ..utils import utils
from app import mqtt



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
            #print("RES0" + data)
            if data == None:
                return {'message': 'No data available'}, 401
            else:
                #type = Utils.getTypeMD(), email = None, username = None, password = None, name = "", lastname = "", photo = ""
                #user = User(data['type'],data['email'],data['username'],data['password'],data['name'],data['lastname'],data['photo'])
                #res=user.save()
                #print(str(data['anomaly']) +"   "+str(type(data['anomaly'])))
                #print("RES" + str(data))
                event = Event(data['name'],data['type'],data['comments'],data['anomaly'])
                res = event.save()

                if res == True:
                    if(data['type']==utils.Utils.TYPE_STRESS):
                        event_stress = EventStress(event.idevent,data['value'])
                        res = event_stress.save()
                    if (data['type'] == utils.Utils.TYPE_ACTIVITY):
                        event_activity = EventActivity(event.idevent, data['value'])
                        res = event_activity.save()
                    if (data['type'] == utils.Utils.TYPE_RESPIRATION):
                        event_respiration = EventRespiration(event.idevent, data['value'])
                        res = event_respiration.save()
                    if res==True:
                        return {"success":'Event created!'}, 200
                    else:
                        return {'message': 'Error creating event'}, 403
                else:
                    return {'message': 'Error creating event'}, 403
        except Exception:
            traceback.print_exc()
            return {'message': 'Error creating event (data missed or already registered)'}, 403



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
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
        camRgb.setVideoSize(640, 480)
        ve2 = pipeline.createVideoEncoder()
        camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

        ve2.setDefaultProfilePreset(640, 480, 24, dai.VideoEncoderProperties.Profile.H265_MAIN)
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
            '''
            fps = 30
            width = 1280
            height = 720
            rtmp_url = "rtmp://f20693752813476f9c882f8290818264.channel.media.azure.net:1935/live/865eede88387412ab08c092b2d9d8713/mystream"

            command = ['ffmpeg',
                       '-y',
                       '-f', 'rawvideo',
                       '-vcodec', 'rawvideo',
                       '-pix_fmt', 'bgr24',
                       '-s', "{}x{}".format(width, height),
                       '-r', str(fps),
                       '-i', '-',
                       '-c:v', 'libx264',
                       '-pix_fmt', 'yuv420p',
                       '-preset', 'ultrafast',
                       '-f', 'flv',
                       rtmp_url]
            p = subprocess.Popen(command, stdin=subprocess.PIPE)
            '''
            while True:
                inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived
                frame = inRgb.getCvFrame() # read the camera frame

                ret, buffer = cv2.imencode('.jpg', frame)
                #print(buffer.shape)

                frame = buffer.tobytes()
                #print("tamanio en kbs",len(frame)/1024.0)
                mqtt.publishMsg("caleta/streaming",frame)
                #print("ernviando")
                #p.stdin.write(frame)
                #print(frame.hex())

                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
                #aux = str(frame)
                #aux = frame.hex()
                #print(aux)
                #mqtt.publishMsg("caleta/streaming",aux)
                #if(mqtt!=None):
                #mqtt.publishMsg("caleta/streaming",frame)
                # command and params for ffmpeg

                '''
                props={}
                # optional: assign system properties
                props.update(messageId = "message_%d" % 1)
                props.update(correlationId = "correlation_%d" % 1)
                props.update(contentType = "application/json")

                # optional: assign application properties
                prop_text = "PropMsg_%d" % 1
                props.update(testProperty = prop_text)

                registry_manager.send_c2d_message(DEVICE_ID, frame, properties=props)
                '''


@public_bp.route('/video_feed',methods=['GET'])
def video_feed():
    #gen_frames()
    #return {"success":''}, 200
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@public_bp.route('/oak')
def index():
    """Video streaming home page."""
    print("aqui")
    return render_template('indexcamera.html')

@public_bp.route('/home')
def home():
    """Video streaming home page."""
    return {"success":'home!'}, 200


@public_bp.route('/')
def mainindex():
    """Video streaming home page."""
    return {"success":'home!'}, 200



'''
@public_bp.route('/')
def index():
    return render_template('indexcamera.html')

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