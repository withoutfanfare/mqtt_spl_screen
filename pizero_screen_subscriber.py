#
#
#
import os
import logging
import paho.mqtt.client as mqtt
from spl_screen import SPScreen
from pizero_screen_config import pizero_screen_config

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

#
# Get Config
#
MQTT_BROKER = pizero_screen_config["mqtt_broker"]
MQTT_TOPIC = pizero_screen_config["mqtt_topic"]
MQTT_PORT = pizero_screen_config["mqtt_port"]

#
# Defaults
#
defaultBg = (16, 23, 31)
initBg = (78, 3, 97)
errorBg = (115, 11, 0)
successBg = (0, 102, 42)
pendingBg = (94, 0, 115)
defaultColor = '#FFFFFF'

#
# MiniPiTft
#
myScreen = SPScreen()

#
# MQTT Client will listen for topic set in config
#
client = mqtt.Client()

#
#
#
def connectMessage(msg):
    myScreen.message(msg, defaultColor, initBg)

#
#
#
def upMessage(msg):
    myScreen.message(msg, defaultColor, successBg)

#
#
#
def downMessage(msg):
    myScreen.message(msg, defaultColor, errorBg)

#
#
#
def heartbeatMessage(msg):
    myScreen.message(msg, defaultColor, pendingBg)

#
#
#
def rebootMessage(msg):
    myScreen.message(msg, defaultColor, defaultBg)

#
#
#
def shutdownMessage(msg):
    myScreen.message(msg, defaultColor, defaultBg)

#
#
#
def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)
    return connectMessage('Connected')

#
#
#
def on_message(client, userdata, msg):
    m = msg.payload.decode('utf-8')
    if "UP @" in m:
        return upMessage(m)
    if "DOWN @" in m:
        return downMessage(m)
    if "OK" in m:
        return heartbeatMessage(m)
    if "REBOOT" in m:
        os.system("sudo systemctl reboot -i")
        return rebootMessage(m)
    if "SHUTDOWN" in m:
        os.system("sudo shutdown -h now")
        return shutdownMessage(m)


#
# Callbacks
#
client.on_connect = on_connect
client.on_message = on_message

#
# Connect and loop
#
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()
