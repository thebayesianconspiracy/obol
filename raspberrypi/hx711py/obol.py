import RPi.GPIO as GPIO
import time
import json
import sys
from hx711 import HX711
import paho.mqtt.client as paho

deviceID = "PI_2"
appID = "APP_1"
hx = HX711(23, 24)

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def on_publish(client, userdata, mid):
    print("published : "+str(mid))
 
def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    client.disconnect()
    print "Bye!"
    sys.exit()

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
 
def on_message(client, userdata, msg):
    jsonMsg = json.loads(str(msg.payload))
    if(jsonMsg['deviceID']==deviceID):
        hx.tare()
        print("Tare")
    print(jsonMsg['deviceID']) 

class Payload:
    deviceID = ""
    appID = ""
    weight = 0
    def __init__(self, deviceID, appID):
        self.deviceID = deviceID
        self.appID = appID
    def setWeight(self,weight):
        self.weight = weight
        
client = paho.Client(client_id="pi_device_1")
client.on_publish = on_publish
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

broker_local = "192.168.43.157"
broker_net = "broker.mqttdashboard.com"

client.connect(broker_local, 1883)
client.subscribe("obol/tare", qos=0)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(92)

hx.reset()
hx.tare()

packet = Payload(deviceID,appID)

while True:
    try:
        val = hx.get_weight(5)
        print val
        hx.power_down()
        hx.power_up()
        packet.setWeight(val)
        client.publish("obol/weight", json.dumps(packet.__dict__), qos=0)
        client.loop()
        time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
