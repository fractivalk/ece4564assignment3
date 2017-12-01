
from flask import Flask, render_template, request
import json
import logging
import socket
import sys
from time import sleep
from zeroconf import ServiceInfo, Zeroconf
import RPi.GPIO as GPIO
import json

the_ip = "192.168.1.22"


# GPIO LEDs
# intensity
# command line IP address???
# advertise correct information
# Services integration and browsing for right advertisement

# POST curl command
""" curl -d '{"color":"magenta", "status":"on", "intensity":"60"}' -H "Content-Type: application/json" -X POST http://172.29.85.191:5000/LED """

# GET curl command
""" curl http://172.29.85.191:5000/LED """

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

red = 4
green = 18
blue = 23

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100
RED = GPIO.PWM(red, Freq)
GREEN = GPIO.PWM(green, Freq)
BLUE = GPIO.PWM(blue, Freq)

RED.start(100)
GREEN.start(0)
BLUE.start(0)


LED_status = 'off'
LED_color = 'red'
LED_intensity = '0'

app = Flask(__name__)


@app.route("/")
def main():
    # return render_template('main.html')
    return "Hello World!"

@app.route("/LED", methods=['GET', 'POST'])
def LED():
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        if 'color' in data.keys() and 'status' in data.keys() and 'intensity' in data.keys():
            global LED_status
            global LED_color
            global LED_intensity
            if data['status'] == 'on':
                if int(data['intensity']) > 100 or int(data['intensity']) < 0:
                    return 'Invalid intensity given\n'
                LED_status = 'on'

                GREEN.ChangeDutyCycle(0)
                RED.ChangeDutyCycle(0)
                BLUE.ChangeDutyCycle(0)
                if data['color'] == 'red':
                    RED.ChangeDutyCycle(100)
                    LED_color = 'Red'
                elif data['color'] == 'green':
                    GREEN.ChangeDutyCycle(100)
                    LED_color = 'Green'
                elif data['color'] == 'blue':
                    BLUE.ChangeDutyCycle(100)
                    LED_color = 'Blue'
                elif data['color'] == 'magenta':
                    RED.ChangeDutyCycle(100)
                    BLUE.ChangeDutyCycle(100)
                    LED_color = 'Magenta'
                elif data['color'] == 'cyan':
                    GREEN.ChangeDutyCycle(100)
                    BLUE.ChangeDutyCycle(100)
                    LED_color = 'Cyan'
                elif data['color'] == 'yellow':
                    RED.ChangeDutyCycle(100)
                    GREEN.ChangeDutyCycle(100)
                    LED_color = 'Yellow'
                elif data['color'] == 'white':
                    RED.ChangeDutyCycle(100)
                    GREEN.ChangeDutyCycle(100)
                    BLUE.ChangeDutyCycle(100)
                    LED_color = 'White'
                else:
                    return 'Color not supported\n'
            elif data['status'] == 'off':
                LED_status = 'off'
                GREEN.ChangeDutyCycle(0)
                RED.ChangeDutyCycle(0)
                BLUE.ChangeDutyCycle(0)
            else:
                return 'Invalid status given\n'
            LED_intensity = int(data['intensity'])
            return 'CHANGED LED\nColor: ' + data['color'] + '\nStatus: ' + data['status'] + '\nIntensity: ' + str(data['intensity']) + '\n'
        else:
            return 'Invalid arguments\n'
    else:
        return 'LED STATE\nColor: ' + LED_color + '\nStatus: ' + LED_status + '\nIntensity: ' + str(LED_intensity) + '\n'


if __name__ == "__main__":

    # ZER0CONF
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    colors = 'red blue green magenta cyan yellow white'

    desc = dict(path='/LED', colors=colors)

    info = ServiceInfo("_http._tcp.local.",
                       "GROUP13LED._http._tcp.local.",
                       socket.inet_aton(the_ip), 5000, 0, 0,
                       desc, "ash-2.local.")

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)

    # APP
    try:
        app.run(host=the_ip, port=5000, debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()
