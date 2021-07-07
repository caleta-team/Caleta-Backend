from paho.mqtt import client as mqtt
import ssl

path_to_root_cert = "/home/bihut/dev/CaletaTeam/Caleta-Backend-v2/app/borrar/certs.c"
device_id = "pi-caleta-1"
sas_token = "HostName=iot-hub-caleta.azure-devices.net;DeviceId=pi-caleta-1;SharedAccessSignature=SharedAccessSignature sr=iot-hub-caleta.azure-devices.net%2Fdevices%2Fpi-caleta-1&sig=nXq60zirDFV8yDPU5cxYJCbwgm%2BvXqTsQ7KE%2Fsnn8kk%3D&se=1625655667"
iot_hub_name = "iot-hub-caleta"


def on_connect(client, userdata, flags, rc):
    print("Device connected with result code: " + str(rc))


def on_disconnect(client, userdata, rc):
    print("Device disconnected with result code: " + str(rc))


def on_publish(client, userdata, mid):
    print("Device sent message")


client = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.username_pw_set(username=iot_hub_name+".azure-devices.net/" +
                       device_id + "/?api-version=2018-06-30", password=sas_token)

cert_file = "/home/bihut/dev/CaletaTeam/certificates/python-device.pem"
key_file = "/home/bihut/dev/CaletaTeam/certificates/python-device.key.pem"
client.tls_set(ca_certs=path_to_root_cert, certfile=cert_file, keyfile=key_file,
               cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
#client.tls_set("/home/bihut/dev/CaletaTeam/certificates/python-device.pem") # use builtin cert on Raspbian

#client.tls_insecure_set(False)

client.connect(iot_hub_name+".azure-devices.net", port=8883)

client.publish("devices/" + device_id + "/messages/events/", '{"id":123}', qos=1)
client.loop_forever()