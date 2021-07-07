import threading
import time
from azure.iot.device import IoTHubDeviceClient

RECEIVED_MESSAGES = 0
CONNECTION_STRING = "HostName=iot-hub-caleta.azure-devices.net;DeviceId=pi-caleta-1;SharedAccessKey=rV8QZs6KLql9CWkioShQs3D2czfsrc0OC07ETSoEUGA="
def message_listener(client):
    global RECEIVED_MESSAGES
    while True:
        message = client.receive_message()
        print(type(message))
        message2 = ""
        RECEIVED_MESSAGES += 1
        print("\nMessage received:")

        #print data and both system and application (custom) properties
        for property in vars(message).items():
            print ("    {0}".format(property))

        print( "Total calls received: {}".format(RECEIVED_MESSAGES))
        print("message2")
        print(message.data)
        message2 = message.data.decode("utf-8")
        print(message2)
        print()

def iothub_client_sample_run():
    try:
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        message_listener_thread = threading.Thread(target=message_listener, args=(client,))
        message_listener_thread.daemon = True
        message_listener_thread.start()

        while True:
            time.sleep(1000)

    except KeyboardInterrupt:
        print ( "IoT Hub C2D Messaging device sample stopped" )

if __name__ == '__main__':
    print ( "Starting the Python IoT Hub C2D Messaging device sample..." )
    print ( "Waiting for C2D messages, press Ctrl-C to exit" )

    iothub_client_sample_run()