import random

from paho.mqtt import client as mqtt_client


class MQTTCaleta():
    BROKER_ADDRESS="vai.uca.es"
    BROKER_PORT=1883
    client=None
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    def __init__(self,id=""):
        super().__init__()
        self.client = mqtt_client.Client(self.client_id)
        #self.client.on_log = self.on_log
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect

        self.client.connect(self.BROKER_ADDRESS, self.BROKER_PORT)
        #self.client.connect(self.BROKER_ADDRESS,self.BROKER_PORT)  # connect to broker
        #self.client.loop_start()

        #self.test()
        #self.client.loop_forever()
        self.client.loop_start()

    def on_subscribe(self,client, userdata, mid, granted_qos):
        print('Subscribed for m' + str(mid))

    def on_log(self,client, userdata, level, buf):
        print("log: ", buf)

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def unsubscribe(self,topic):
        self.client.unsubscribe(topic)

    def publishMsg(self,topic,msg):
        self.client.publish(topic,msg,qos=0, retain=False)

    def on_message(self,client, userdata, message):
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)
        print("message qos=", message.qos)
        print("message retain flag=", message.retain)
        print (" - ".join((message.topic, str(message.payload))))
        # Do this only if you want to send a reply message every time you receive one
        #client.publish("devices/<YOUR DEVICE ID>/messages/events", "REPLY", qos=1)
    '''
    def test(self):
        # Publish
        time.sleep(1)
        for x in range(3):
            exp = datetime.datetime.utcnow()
            abcstring1 = {
                "AI01": 17*x
            }
            data_out1 = json.dumps(abcstring1)
            self.client.publish("devices/{device_id}/messages/events/".format(device_id=self.device_id), payload=data_out1, qos=1,
                           retain=False)
            print("Publishing on devices/" + self.device_id + "/messages/events/", data_out1)
            time.sleep(5)
            
    '''