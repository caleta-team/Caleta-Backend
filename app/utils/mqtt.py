import paho.mqtt.client as mqtt

class MQTTCaleta():
    BROKER_ADDRESS="localhost"
    BROKER_PORT=1883
    client=None

    def __init__(self,id=""):
        super().__init__()
        self.client = mqtt.Client(id)  # create new instance
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.connect(self.BROKER_ADDRESS,self.BROKER_PORT)  # connect to broker
        self.client.loop_start()
        #self.client.loop_forever()

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        #subscribe channels here
        #client.subscribe("$SYS/#")
        client.subscribe("prueba/caleta")
        print("suscrito")

    def unsubscribe(self,topic):
        self.client.unsubscribe(topic)

    def publishMsg(self,topic,msg):
        self.client.publish(topic,msg,qos=0, retain=False)

    def on_message(self,client, userdata, message):
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)
        print("message qos=", message.qos)
        print("message retain flag=", message.retain)