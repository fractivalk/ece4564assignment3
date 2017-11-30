
from flask import Flask, render_template, request
import json
import logging
import socket
import sys
from time import sleep
from zeroconf import ServiceInfo, Zeroconf
import RPi.GPIO as GPIO
import json


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


app = Flask(__name__)


@app.route("/")
def main():
    # return render_template('main.html')
    return "Hello World!"


@app.route("/LED", methods=['GET', 'POST'])
def LED():
    if request.method == 'POST':
        data = json.loads(request.data)
        LED_color = data['color']
        LED_status = data['status']
        if LED_status == 'on':
            GREEN.ChangeDutyCycle(0)
            RED.ChangeDutyCycle(0)
            BLUE.ChangeDutyCycle(0)
            if LED_color == 'red':
                RED.ChangeDutyCycle(100)
            elif LED_color == 'green':
                GREEN.ChangeDutyCycle(100)
            elif LED_color == 'blue':
                BLUE.ChangeDutyCycle(100)
            elif LED_color == 'magenta':
                RED.ChangeDutyCycle(100)
                BLUE.ChangeDutyCycle(100)
            elif LED_color == 'cyan':
                GREEN.ChangeDutyCycle(100)
                BLUE.ChangeDutyCycle(100)
            elif LED_color == 'yellow':
                RED.ChangeDutyCycle(100)
                GREEN.ChangeDutyCycle(100)
            elif LED_color == 'white':
                RED.ChangeDutyCycle(100)
                GREEN.ChangeDutyCycle(100)
                BLUE.ChangeDutyCycle(100)
        elif LED_status == 'off':
            GREEN.ChangeDutyCycle(0)
            RED.ChangeDutyCycle(0)
            BLUE.ChangeDutyCycle(0)
        return 'Changed LED to: ' + data['color'] + data['status']
    else:
        return 'LED status: < Display Here >'


if __name__ == "__main__":

    # ZER0CONF
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    desc = {'path': '/LED/'}

    info = ServiceInfo("_http._tcp.local.",
                       "COLINSLED._http._tcp.local.",
                       socket.inet_aton("127.0.0.1"), 80, 0, 0,
                       desc, "ash-2.local.")

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)

    # APP
    try: # 172.29.33.66
        app.run(host='172.29.102.146', port=5000, debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()
