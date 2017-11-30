import time
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import json

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

red = 23
green = 18
blue = 4

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100
RED = GPIO.PWM(red, Freq)
GREEN = GPIO.PWM(green, Freq)
BLUE = GPIO.PWM(blue, Freq)

RED.start(100)
GREEN.start(100)
BLUE.start(100)

def color(R, G, B, on_time):
    # Color brightness range is 0-100%
    RED.ChangeDutyCycle(R)
    GREEN.ChangeDutyCycle(G)
    BLUE.ChangeDutyCycle(B)
    time.sleep(on_time)

    # Turn all LEDs off after on_time seconds
    RED.ChangeDutyCycle(0)
    GREEN.ChangeDutyCycle(0)
    BLUE.ChangeDutyCycle(0)
    time.sleep(on_time)
try:
    while 1:
        color(50, 10, 30, 1)
except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()
