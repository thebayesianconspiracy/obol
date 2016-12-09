import RPi.GPIO as GPIO
import time
import json
import sys
from hx711 import HX711
import paho.mqtt.client as paho
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

def on_publish(client, userdata, mid):
    print("published : "+str(mid))
 
client = paho.Client(client_id="pi_device_1")
client.on_publish = on_publish
client.on_connenct = on_connect
broker_local = "192.168.43.157"
broker_net = "broker.mqttdashboard.com"
client.connect(broker_local, 1883)
client.loop_start()

def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    client.disconnect()
    print "Bye!"
    sys.exit()

hx = HX711(23, 24)


# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("LSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
hx.set_reference_unit(92)

hx.reset()
hx.tare()

while True:
    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment the three lines to see what it prints.
        #np_arr8_string = hx.get_np_arr8_string()
        #binary_string = hx.get_binary_string()
        #print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = hx.get_weight(5)
        print val

        hx.power_down()
        hx.power_up()
        payload = { 'properties': [{ 'app_id': 'app_1', 'device_id': 'pi_device_1', 'weight': val }] }
        client.publish("yoyo123", json.dumps(payload), qos=0)
        time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
