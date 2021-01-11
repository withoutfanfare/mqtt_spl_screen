import paho.mqtt.client as mqtt
import os
import logging

import digitalio
import board

from spl_screen import SPScreen
from pizero_screen_config import pizero_screen_config

logging.basicConfig(filename='/tmp/debug.log', level=logging.DEBUG)

MQTT_BROKER = pizero_screen_config["mqtt_broker"]
# MQTT_TOPIC = pizero_screen_config["mqtt_topic"]
MQTT_PORT = pizero_screen_config["mqtt_port"]

MQTT_TOPIC = [(pizero_screen_config['mqtt_topic'],2),('/ble/battery/puck',1)]

defaultBg = (16, 23, 31)
initBg = (78, 3, 97)
errorBg = (115, 11, 0)
successBg = (0, 102, 42)
pendingBg = (94, 0, 115)

defaultColor = '#FFFFFF'

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB.switch_to_input(pull=digitalio.Pull.UP)

pressedA = 0
pressedB = 0

myScreen = SPScreen()
client = mqtt.Client()

myScreen.message("Initialising...", defaultColor, defaultBg)

def on_connect(client, userdata, flags, rc):
    # logger.info("Connected with result code " + str(rc))
    myScreen.message('Connected.', defaultColor, initBg)
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    m = msg.payload.decode('utf-8')
    bg = defaultBg
    if "UP @" in m:
        bg = successBg
    if "DOWN @" in m:
        bg = errorBg
    if "OK" in m:
        bg = pendingBg
    if "HEARTBEAT" in m:
        bg = pendingBg
    if "TEMP" in m:
        bg = pendingBg
    if "REBOOT" in m:
        os.system("sudo systemctl reboot -i")
    if "99" in m:
        myScreen.message('REBOOT', errorBg, bg)
        os.system("sudo systemctl reboot -i")
    if 99 in m:
        myScreen.message('REBOOT', errorBg, bg)
        os.system("sudo systemctl reboot -i")
    if "98" in m:
        myScreen.message('SHUTDOWN', errorBg, bg)
        os.system("sudo shutdown -h now")
    if 98 in m:
        myScreen.message('SHUTDOWN', errorBg, bg)
        os.system("sudo shutdown -h now")
    if "SHUTDOWN" in m:
        os.system("sudo shutdown -h now")

    myScreen.message(m, defaultColor, bg)


client.on_connect = on_connect
client.on_message = on_message

if buttonB.value and not buttonA.value:
    if pressedB == 0:
        pressedB = 1
        myScreen.message("Reboot", defaultColor, pendingBg)
        check_call(['sudo', 'reboot'])
        pressedB = 0
if buttonA.value and not buttonB.value:
    if pressedA == 0:
        pressedA = 1
        myScreen.message("Shutdown", defaultColor, pendingBg)
        check_call(['sudo', 'poweroff'])
        pressedA = 0

client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_forever()

