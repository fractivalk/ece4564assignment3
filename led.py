import time
import RPi.GPIO as GPIO
from flask import Flask, render_template, request

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

red = 4
green = 17
blue = 27

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100
RED = GPIO.PWM(red, Freq)
GREEN = GPIO.PWM(green, Freq)
BLUE = GPIO.PWM(blue, Freq)

RED.start(50)
GREEN.start(10)
BLUE.start(30)

@app.route("/")
def main():
   # return render_template('main.html')
   return "Hello World!"

@app.route("/LED")
def LED():
    status =    request.args.get('status', default = '', type = str)
    color =     request.args.get('color', default = '', type = str)
    intensity = request.args.get('intensity', default = 0, type = int)
    if status == "on":
        GREEN.ChangeDutyCycle(0)
        RED.ChangeDutyCycle(0)
        BLUE.ChangeDutyCycle(0)
        if color == 'red':
            RED.ChangeDutyCycle(intensity)
        elif color == 'green':
            GREEN.ChangeDutyCycle(intensity)
        elif color == 'blue':
            BLUE.ChangeDutyCycle(intensity)
    if status == "off":
        GREEN.ChangeDutyCycle(0)
        RED.ChangeDutyCycle(0)
        BLUE.ChangeDutyCycle(0)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
