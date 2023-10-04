#
#   Weather update server
#   Binds PUB socket to tcp://*:5556
#   Publishes random weather updates
#

import zmq
from random import randrange


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5557")

while True:
    # generate 4 digit zipcode and random temp
    zipcode = randrange(1000, 10000)
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)

    socket.send_string(f"PT {zipcode} {temperature} {relhumidity}")