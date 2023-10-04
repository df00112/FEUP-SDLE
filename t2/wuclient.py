#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys
import zmq


#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather servers")

# Connect to US server
socket.connect("tcp://localhost:5556")

# Connect to PT server
socket.connect("tcp://localhost:5557")

socket.setsockopt_string(zmq.SUBSCRIBE, "")

# Poller to handle multiple sockets
poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

# Process 5 updates
total_temp = 0
update_nbr = 0

while True:
    socks = dict(poller.poll())

    if socket in socks and socks[socket] == zmq.POLLIN:
        string = socket.recv_string()
        server_id, zipcode, temperature, relhumidity = string.split()
        total_temp += int(temperature)
        update_nbr += 1

        print(f"From: {server_id}, Zipcode: {zipcode}, Temperature: {temperature}, Relative Humidity: {relhumidity}")
        if update_nbr == 10:
            break
print(f"Average temperature for all zipcodes: {total_temp / update_nbr} F")