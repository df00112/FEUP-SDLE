# Simple request-reply broker
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import zmq

# Prepare our context and sockets
context = zmq.Context()
frontend = context.socket(zmq.XPUB)
frontend.bind("tcp://*:5559")

backend = context.socket(zmq.XSUB)
backend.bind("tcp://*:5560")

print("Starting broker...")

zmq.proxy(frontend, backend)
'''
poller = zmq.Poller()
poller.register(frontend, zmq.POLLIN)
poller.register(backend, zmq.POLLIN)

while True:
    print("B4 try")
    try:
        socks = dict(poller.poll())

        if socks.get(frontend) == zmq.POLLIN:
            message = frontend.recv()
            backend.send(message)
        elif socks.get(backend) == zmq.POLLIN:
            message = backend.recv()
            frontend.send(message)
    except KeyboardInterrupt:
        break
'''

# We never get here...
frontend.close()
backend.close()
context.term()

