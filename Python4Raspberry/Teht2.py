import RPi.GPIO as GPIO
import time
#pin def
ledPin = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.HIGH)
time.sleep(2)
GPIO.cleanup()
