import json
import datetime
import time


import paho.mqtt.client as mqtt

class MQTTCaleta():
    BROKER_ADDRESS="localhost"
    BROKER_PORT=1883
    client=None
    device_id = "pi-caleta-1"  # Add device id
    iot_hub_name = "iot-hub-caleta"  # Add iot hub name
    sas_token = "HostName=iot-hub-caleta.azure-devices.net;DeviceId=pi-caleta-1;SharedAccessSignature=SharedAccessSignature sr=iot-hub-caleta.azure-devices.net%2Fdevices%2Fpi-caleta-1&sig=YxbaaisXkNYg2CwOWlGTVUyIBusyMIa6jDSFSgBstEE%3D&se=1625590335"  # Add sas token string

    def __init__(self,id=""):
        super().__init__()
        self.client = mqtt.Client(client_id=self.device_id, protocol=mqtt.MQTTv311)
        self.client.on_log = self.on_log
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        username = "{}.azure-devices.net/{}".format(self.iot_hub_name, self.device_id)
        print("username:",username)
        self.client.username_pw_set(username=username, password=self.sas_token)

        # Connect to the Azure IoT Hub
        self.client.connect(self.iot_hub_name + ".azure-devices.net", port=8883)
        #self.client.connect(self.BROKER_ADDRESS,self.BROKER_PORT)  # connect to broker
        #self.client.loop_start()

        print("suscrito")
        self.test()
        self.client.loop_forever()

    def on_subscribe(self,client, userdata, mid, granted_qos):
        print('Subscribed for m' + str(mid))

    def on_log(self,client, userdata, level, buf):
        print("log: ", buf)

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("devices/{device_id}/messages/devicebound/#".format(device_id=self.device_id))

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