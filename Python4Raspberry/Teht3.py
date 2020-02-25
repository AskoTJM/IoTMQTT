import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(18) == False:
        print("Nappi 1 Toimii!!")
        time.sleep(0.2)
    if GPIO.input(23) == False:
        print("Nappi 2 toimii!!")
        time.sleep(0.2)