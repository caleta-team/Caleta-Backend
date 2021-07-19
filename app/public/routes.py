import json
import queue
import subprocess as sp
import threading
from time import sleep

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
            if data == None:
                return {'message': 'No data available'}, 401
            else:
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


@public_bp.route('/events/<string:type>/<int:starttime>/<int:endtime>',methods=['GET'])
def listEventsQuery(type,starttime,endtime):
    aux = Token.checkAuthorization(request.headers['token'])
    if aux == False:
        return {'message': 'Non Authorised - Not valid token'}, 401
    else:
        if type=="all":
            events = Event.query.filter(Event.create_time >= starttime, Event.create_time <= endtime)
        else:
            events = Event.query.filter(Event.create_time >= starttime, Event.create_time <= endtime,Event.type == type)

        array_result = []
        for event in events.all():
            array_result.append(event.getJSON())

        print(array_result)
        return {'payload': array_result}, 200

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
                #print("RES" + str(data))
                ty = data['type']
                if(ty!= utils.Utils.TYPE_STRESS and ty!=utils.Utils.TYPE_ACTIVITY and ty != utils.Utils.TYPE_RESPIRATION):
                    return {'message': 'Wrong event type'}, 401

                event = Event(data['name'],data['type'],data['comments'],data['anomaly'],data['value'])
                res = event.save()

                if res == True:
                    mqtt.publishMsg(utils.Utils.MQTT_TOPIC_BASE+"/"+data['type'],json.dumps(event.getJSON()))
                    return {"success": 'Event created!'}, 200
                '''
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
                '''
        except Exception:
            traceback.print_exc()
            return {'message': 'Error creating event (data missed or already registered)'}, 403
fps = 30#30
width = 1920
height =1080
frame_queue = queue.Queue()
rtmp_url = "rtsp://localhost:8554/mystream" #"rtmp://localhost:1935/show/stream"
command = ['ffmpeg',
                       '-y',
                       '-f', 'rawvideo',
                       '-vcodec', 'rawvideo',
                       '-pix_fmt', 'bgr24',
                       '-s', "{}x{}".format(width, height),
                       '-i', '-',
                       '-c:v', 'libx264',
                       '-pix_fmt', 'yuv420p',
                       '-preset', 'ultrafast',
                       '-f', 'rtsp',
                       rtmp_url]
p = None
def push_frame():
        global command, frame_queue, p

        while True:
            if len(command) > 0:
                p = sp.Popen(command, stdin=sp.PIPE)
                break

        while True:
            if frame_queue.empty() != True:
                frame = frame_queue.get()
                # process frame
                # write to pipe
                p.stdin.write(frame.tostring())
                #print("escrito")


def gen_frames():  # generate frame by frame from camera
    #p = sp.Popen(command, stdin=sp.PIPE)
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
        camRgb.setInterleaved(False)
        camRgb.setPreviewSize(width, height)
        camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        camRgb.setVideoSize(width, height)
        ve2 = pipeline.createVideoEncoder()



        ve2.setDefaultProfilePreset(width, height, fps, dai.VideoEncoderProperties.Profile.MJPEG)
        camRgb.video.link(ve2.input)

        #camRgb.setVideoSize(width,height)

        xoutVideo.input.setBlocking(False)
        xoutVideo.input.setQueueSize(1)

        # Linking
        camRgb.video.link(xoutVideo.input)


        with dai.Device(pipeline) as device:
            # Output queue will be used to get the rgb frames from the output defined above
            qRgb = device.getOutputQueue(name="video", maxSize=1, blocking=False)

            while True:
                inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived
                frame = inRgb.getCvFrame() # read the camera frame
                #cv2.imshow("bgr", frame)
                ret, buffer = cv2.imencode('.jpg', frame)

                new_w = 600
                #frame = cv2.resize(frame, (new_w, new_h))

                if not ret:
                    print("Opening camera is failed")
                    # Para ser honesto, la ruptura aquí debería ser reemplazada por:
                    # cap = cv.VideoCapture(self.camera_path)
                    # Porque hubo un problema con el flujo del proyecto que encontré en los últimos dos días
                    # ¡Especialmente al extraer secuencias rtmp! ! ! !
                    pass
                else:
                    frame_queue.put(frame) # ha funcionando una vez
                    #print("enviando mqtt")

                    #mqtt.publishMsg("caleta/stream",buffer.tostring())

                #frame = buffer.tobytes()


                #yield (b'--frame\r\n'
                #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result



@public_bp.route('/video_feed',methods=['GET'])
def video_feed():
    #gen_frames()
    #return {"success":''}, 200
    #return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    try:
        threads = [
            threading.Thread(target=gen_frames, args=()),
            threading.Thread(target=push_frame, args=())
        ]
        [thread.setDaemon(True) for thread in threads]
        [thread.start() for thread in threads]
        return {'message': 'ok'}, 200
    except:
        return {'message': 'error'}, 401



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