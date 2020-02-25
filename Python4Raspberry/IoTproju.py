# 23.02.2020
# Kurssi: IoT-ohjelmoinnin perusteet Projekti
# Tekijät: Mattila, Asko ja Mehtälä, Jussi
# Kuvaus: Kesämökin etävalvonta, halvalla.
# Toteutus: Projektissa käytettiin Raspberry Pi:tä, johon kytkettiin kytkentäalustan avulla
# GPIO-liitäntään kaksi nappulaa, ledi sekä lämpötila-anturi. Yksi napeista kuvaa ovi-anturia,
# jota painaessa simuloidaan oven auki oloa. Toinen napeista ohjaa lediä, joka kuvastaa mökin valoja.
# Lämpötila-anturi mittaa mökin lämpötilaa. Raspberry Pi kerää näiden tiedot ja lähettää ne
# CloudMQTT-palvelimelle. Jonka kanavia seuraa Android sovellus.

import os
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from apscheduler.schedulers.background import BackgroundScheduler

sched= BackgroundScheduler(daemon=True)

# Temperature modprobe
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
# Lämpötila anturin tiedosto
temp_sensor = '/sys/bus/w1/devices/22-0000005740da/w1_slave'

# Stuff for buttons
GPIO.setmode(GPIO.BCM)
# Doorbell button
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Led control button
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Määritellään ledin Pinni 
ledPin = 20
# Määritellään Ledi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.LOW)


# Luetaan lämpötila anturin raaka data.
def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Luetaan lämpötilat anturilta ja muutetaan käytännölliseen muotoon.
def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c #, temp_f

# Mqtt yhteyden aloittamisen määrittelyjä.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
# Subscribetaan kanavalle josta saadaan ledin ohjausta.    
    client.subscribe("ledscontrol")

# Mitä tehdään kun viesti saapuu.
def on_message(client, userdata, msg):
#Tulostetaan debuggausta varten viestin sisältö.
    print(msg.topic+" "+str(msg.payload))
#Jos viestillä tarkoitus ohjata lediä.
    if msg.topic == "ledscontrol":
        led_toggle()

        ##rrint(GPIO.input(ledPin))

# Led toggling jos led päälle se sammutetaan, jos ei se laitetaan päälle
def led_toggle():
    if GPIO.input(ledPin) == GPIO.HIGH:
           print("Vintti pimeeksi")
           client.publish("leds","Off",2, False, None)
           GPIO.output(ledPin, GPIO.LOW)
    else:
           print("Valoa kansalle")
           client.publish("leds","On",2, False, None)
           GPIO.output(ledPin, GPIO.HIGH)

# Door toggling, jos ovi auki lähetetään MQTT viestejä kunnes se suljetaan.
def toggle_door():
    doorOpenLocal = doorOpen
    if GPIO.input(18) == GPIO.LOW:
        client.publish("doorbell","OPEN",2,False,None)
        doorOpenLocal = True
        time.sleep(0.2)
    if (doorOpenLocal == True & GPIO.input(18) == GPIO.HIGH):
        client.publish("doorbell","close",2,False,None)
        time.sleep(0.2)

# Lähetään lämpötila MQTT palvelimelle
def send_temp():
    temp = str(read_temp())   
    client.publish("temperature",temp,2, False, None)
    
# Mqtt stuff 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# MQTT palvelimen asetukset
client.connect("hairdresser.cloudmqtt.com", 16411, 60)
client.username_pw_set("pkrqoggu", "j2qz4gfCubhL")

#Aloitetaan looppi
client.loop_start()
# Arvojen alustaminen ja lähettäminen MQTT palvelimelle.
client.publish("temperature","--",2, False, None)
client.publish("leds","--",2, False, None)
client.publish("doorbell","--",2, False, None)

doorOpen = False
# Ajastetaan scheduler mittaamaan lämpötilan määrätyllä aikavälillä. 
sched.add_job(send_temp,'interval',seconds=3)
sched.start()

#
while True:
    #if GPIO.input(18) == False:
    toggle_door()
   
    if GPIO.input(23) == False:
        led_toggle()
        time.sleep(0.2)
                    
