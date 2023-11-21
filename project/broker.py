#
##  Paranoid Pirate queue
#
#   Author: Daniel Lundin <dln(at)eintr(dot)org>
#

from collections import OrderedDict
import time

import zmq

HEARTBEAT_LIVENESS = 3     # 3..5 is reasonable
HEARTBEAT_INTERVAL = 1.0   # Seconds

#  Paranoid Pirate Protocol constants
PPP_READY = b"\x01"      # Signals server is ready
PPP_HEARTBEAT = b"\x02"  # Signals server heartbeat


class Server(object):
    def __init__(self, address):
        self.address = address
        self.expiry = time.time() + HEARTBEAT_INTERVAL * HEARTBEAT_LIVENESS

class ServerQueue(object):
    def __init__(self):
        self.queue = OrderedDict()

    def ready(self, server):
        self.queue.pop(server.address, None)
        self.queue[server.address] = server

    def purge(self):
        """Look for & kill expired servers."""
        t = time.time()
        expired = []
        for address, server in self.queue.items():
            if t > server.expiry:
                expired.append(address)
        for address in expired:
            print("W: Idle server expired: %s" % address)
            self.queue.pop(address, None)

    def next(self):
        address, server = self.queue.popitem(False)
        return address

context = zmq.Context(1)

frontend = context.socket(zmq.ROUTER) # ROUTER
backend = context.socket(zmq.ROUTER)  # ROUTER
frontend.bind("tcp://*:5555") # For clients
backend.bind("tcp://*:5556")  # For servers

poll_servers = zmq.Poller()
poll_servers.register(backend, zmq.POLLIN)

poll_both = zmq.Poller()
poll_both.register(frontend, zmq.POLLIN)
poll_both.register(backend, zmq.POLLIN)

servers = ServerQueue()

heartbeat_at = time.time() + HEARTBEAT_INTERVAL

while True:
    if len(servers.queue) > 0:
        poller = poll_both
    else:
        poller = poll_servers
    socks = dict(poller.poll(HEARTBEAT_INTERVAL * 1000))

    # Handle server activity on backend
    if socks.get(backend) == zmq.POLLIN:
        # Use server address for LRU routing
        frames = backend.recv_multipart()
        if not frames:
            break

        address = frames[0]
        servers.ready(Server(address))

        # Validate control message, or return reply to client
        msg = frames[1:]
        if len(msg) == 1:
            if msg[0] not in (PPP_READY, PPP_HEARTBEAT):
                print("E: Invalid message from server: %s" % msg)
        else:
            frontend.send_multipart(msg)

        # Send heartbeats to idle servers if it's time
        if time.time() >= heartbeat_at:
            for server in servers.queue:
                msg = [server, PPP_HEARTBEAT]
                backend.send_multipart(msg)
            heartbeat_at = time.time() + HEARTBEAT_INTERVAL
    if socks.get(frontend) == zmq.POLLIN:
        frames = frontend.recv_multipart()
        if not frames:
            break

        frames.insert(0, servers.next())
        backend.send_multipart(frames)


    servers.purge()