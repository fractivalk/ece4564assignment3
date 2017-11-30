from six.moves import input
from zeroconf import ServiceBrowser, Zeroconf
# from __future__ import absolute_import, division, print_function, unicode_literals
from zeroconf import ZeroconfServiceTypes

""" Listing services available """
myName =  ""
class MyListener(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        myName = name
        if str(name) == 'COLINSLED._http._tcp.local.':
            print('Found: ' + str(myName))


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
print (myName)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()




""" Listing service types available """

# print('\n'.join(ZeroconfServiceTypes.find()))




""" Example of announcing a service (in this case, a fake HTTP server) """

# import logging
# import socket
# import sys
# from time import sleep
#
# from zeroconf import ServiceInfo, Zeroconf
#
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG)
#     if len(sys.argv) > 1:
#         assert sys.argv[1:] == ['--debug']
#         logging.getLogger('zeroconf').setLevel(logging.DEBUG)
#
#     desc = {'path': '/~paulsm/'}
#
#     info = ServiceInfo("_http._tcp.local.",
#                        "Paul's Test Web Site._http._tcp.local.",
#                        socket.inet_aton("127.0.0.1"), 80, 0, 0,
#                        desc, "ash-2.local.")
#
#     zeroconf = Zeroconf()
#     print("Registration of a service, press Ctrl-C to exit...")
#     zeroconf.register_service(info)
#     try:
#         while True:
#             sleep(0.1)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         print("Unregistering...")
#         zeroconf.unregister_service(info)
#         zeroconf.close()




""" Example of browsing for a service (in this case, HTTP) """

# import logging
# import socket
# import sys
# from time import sleep
#
# from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
#
#
# def on_service_state_change(zeroconf, service_type, name, state_change):
#     print("Service %s of type %s state changed: %s" % (name, service_type, state_change))
#
#     if state_change is ServiceStateChange.Added:
#         info = zeroconf.get_service_info(service_type, name)
#         if info:
#             print("  Address: %s:%d" % (socket.inet_ntoa(info.address), info.port))
#             print("  Weight: %d, priority: %d" % (info.weight, info.priority))
#             print("  Server: %s" % (info.server,))
#             if info.properties:
#                 print("  Properties are:")
#                 for key, value in info.properties.items():
#                     print("    %s: %s" % (key, value))
#             else:
#                 print("  No properties")
#         else:
#             print("  No info")
#         print('\n')
#
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG)
#     if len(sys.argv) > 1:
#         assert sys.argv[1:] == ['--debug']
#         logging.getLogger('zeroconf').setLevel(logging.DEBUG)
#
#     zeroconf = Zeroconf()
#     print("\nBrowsing services, press Ctrl-C to exit...\n")
#     browser = ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[on_service_state_change])
#
#     try:
#         while True:
#             sleep(0.1)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         zeroconf.close()
