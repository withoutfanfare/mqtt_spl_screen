import paho.mqtt.client as mqtt
import os
import logging

from spl_screen import SPScreen
from pizero_screen_config import pizero_screen_config

logging.basicConfig(filename='/tmp/debug.log', level=logging.DEBUG)

MQTT_BROKER = pizero_screen_config["mqtt_broker"]
MQTT_TOPIC = pizero_screen_config["mqtt_topic"]
MQTT_PORT = pizero_screen_config["mqtt_port"]

defaultBg = (16, 23, 31)
initBg = (78, 3, 97)
errorBg = (115, 11, 0)
successBg = (0, 102, 42)
pendingBg = (94, 0, 115)

defaultColor = '#FFFFFF'

myScreen = SPScreen()
client = mqtt.Client()

myScreen.message("Please Wait", defaultColor, defaultBg)

def on_connect(client, userdata, flags, rc):
    # logger.info("Connected with result code " + str(rc))
    myScreen.message('Connected', defaultColor, initBg)
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    m = msg.payload.decode('utf-8')
    bg = defaultBg
    if "UP @ " in m:
        bg = successBg
    if "DOWN @ " in m:
        bg = errorBg
    if "HEARTBEAT @ " in m:
        bg = pendingBg
    if "REBOOT" in m:
        os.system("sudo systemctl reboot -i")
    if "SHUTDOWN" in m:
        os.system("sudo shutdown -h now")

    myScreen.message(m, defaultColor, bg)


client.on_connect = on_connect
client.on_message = on_message


client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()

