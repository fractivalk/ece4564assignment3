from zeroconf import ServiceBrowser, Zeroconf
import struct
import socket
import requests
#from six.moves import input

ledip = ""
""" Listing services available """
myName =  ""
class MyListener(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)

        myName = name
        if str(name) == 'COLINSLED._http._tcp.local.':
            ip = info.address
            path= ""
            prStr = socket.inet_ntoa(ip)
            #print('Found: ' + str(prStr) + " port: " + str(info.port) + str(info.properties))
            if info.properties:
                print(" Properties Are")
                for key, value in info.properties.items():
                    print (key.decode('UTF-8'))
                    if key.decode("UTF-8") == "path":
                        print ("HI")
                        path = str(value)

            print('http://' + prStr + ":" + str(info.port) + path)

zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
print (myName)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
