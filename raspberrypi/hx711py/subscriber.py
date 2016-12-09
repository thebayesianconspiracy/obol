import json
import time
import sys
import paho.mqtt.client as paho
 
def cleanAndExit():
    print "Cleaning..."
    client.disconnect()
    print "Bye!"
    sys.exit()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
 
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
 
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload)) 

client = paho.Client(client_id="pi_device_2")
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish
client.on_connenct = on_connect
broker_local = "192.168.43.157"
broker_net = "broker.mqttdashboard.com"
client.connect(broker_local, 1883)
client.subscribe("yoyo123", qos=0)
client.loop_forever()
