import time
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from flask.ext.discoverer import Discoverer, advertise
import json

app = Flask(__name__)
discoverer = Discoverer(app)

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

RED.start(0)
GREEN.start(0)
BLUE.start(0)

LED_status = False
LED_color = 'red'

# def color(R, G, B, on_time):
#     # Color brightness range is 0-100%
#     RED.ChangeDutyCycle(R)
#     GREEN.ChangeDutyCycle(G)
#     BLUE.ChangeDutyCycle(B)
#     time.sleep(on_time)
#
#     # Turn all LEDs off after on_time seconds
#     RED.ChangeDutyCycle(0)
#     GREEN.ChangeDutyCycle(0)
#     BLUE.ChangeDutyCycle(0)
#     time.sleep(on_time)
#
# while 1:
#     color(50, 10, 30, 1)


@app.route("/")
def main():
   # return render_template('main.html')
   return "Hello World!"

@advertise(status=["on", "off"],colors=["red","green","blue","magenta","cyan","yellow","white"],intensity='1-100')
@app.route("/LED", methods=['GET', 'POST'])
def LED():
    if (request.method == 'POST'):
        data = json.loads(request.data)
        LED_color = data['color']
        LED_status = data['status']
        if LED_status == 'on':
            GREEN.ChangeDutyCycle(0)
            RED.ChangeDutyCycle(0)
            BLUE.ChangeDutyCycle(0)
            if LED_color == 'red':
                RED.ChangeDutyCycle(data['intensity'])
            elif LED_color == 'green':
                GREEN.ChangeDutyCycle(data['intensity'])
            elif LED_color == 'blue':
                BLUE.ChangeDutyCycle(data['intensity'])
            elif LED_color == 'magenta':
                RED.ChangeDutyCycle(data['intensity'])
                BLUE.ChangeDutyCycle(data['intensity'])
            elif LED_color == 'cyan':
                GREEN.ChangeDutyCycle(data['intensity'])
                BLUE.ChangeDutyCycle(data['intensity'])
            elif LED_color == 'yellow':
                RED.ChangeDutyCycle(data['intensity'])
                GREEN.ChangeDutyCycle(data['intensity'])
            elif LED_color == 'white':
                RED.ChangeDutyCycle(data['intensity'])
                GREEN.ChangeDutyCycle(data['intensity'])
                BLUE.ChangeDutyCycle(data['intensity'])
        elif LED_status == 'off':
            GREEN.ChangeDutyCycle(0)
            RED.ChangeDutyCycle(0)
            BLUE.ChangeDutyCycle(0)
        return 'Changed LED'
    else:
        return ('LED status: ' + LED_status + '\nLED color: ' + LED_color)

if __name__ == "__main__":
    app.run(host='172.29.33.66', port=5000, debug=True)
