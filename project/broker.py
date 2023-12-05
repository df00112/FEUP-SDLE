#
##  Paranoid Pirate queue
#
#   Author: Daniel Lundin <dln(at)eintr(dot)org>
#

from collections import OrderedDict
import sys
import time

import zmq

PROXYLIST=[["tcp://*:5555","tcp://*:5556"],["tcp://*:5557","tcp://*:5558"]]
# 00 and 10 for frontend and 01 and 11 for backend

PING = b"ping" # Client sends this to broker to check if it is alive
LIST_REQUEST=b"\x03" # Client sends this to broker to request a list
LIST_RESPONSE=b"\x04" # Broker sends this to client with the list
LIST_UPDATE=b"\x05" # Client sends this to broker to update the list
LIST_UPDATE_RESPONSE=b"\x06" # Broker sends this to client with the update status
LIST_DELETE=b"\x07" # Client sends this to broker to delete a list
LIST_DELETE_RESPONSE=b"\x08" # Broker sends this to client with the delete status
LIST_CREATE=b"\x09" # Client sends this to broker to create a list
LIST_CREATE_RESPONSE=b"\x10" # Broker sends this to client with the create status
LIST_DELETE_DENIED=b"\x11" # Broker sends this to client when the list owner is not the client

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

def check_request(request):
    
    if(request[0] == PING):
        return [True, request]
    elif(request[0] == LIST_REQUEST):
        return [LIST_REQUEST, request]
    elif(request[0] == LIST_UPDATE):
        return [LIST_UPDATE, request]
    elif(request[0] == LIST_DELETE):
        return [LIST_DELETE, request]
    elif(request[0] == LIST_CREATE):
        return [LIST_CREATE, request]
    return [False,False]



def run():
    global servers
    global poll_servers
    global poll_both
    global heartbeat_at
    global frontend
    global backend
  
    while True:
        # MUDAR ESTE  == QUANDO TIVERMOS SERVERS
        if len(servers.queue) != 0:
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
            print("frames:",frames)
            address = frames[0]
            # VER SE É SUPOSTO MANDAR ISTO SEMPRE
            servers.ready(Server(address))

            # Validate control message, or return reply to client
            msg = frames[1:]
            print("msg:")
            print(msg)
            if len(msg) == 1:
                if msg[0] not in (PPP_READY, PPP_HEARTBEAT):
                    print("E: Invalid message from server: %s" % msg)
                elif msg[0] == PPP_READY:
                    servers.ready(Server(address))
                    
            else:
                address=msg[0]
                msg=msg[1:]
                print("NEW ADDRESS: ",address)
                print("NEW MSG: ",msg)
                frontend.send(address, zmq.SNDMORE)
                frontend.send(b"", zmq.SNDMORE)
                frontend.send_multipart(msg)

            # Send heartbeats to idle servers if it's time
            if time.time() >= heartbeat_at:
                for server in servers.queue:
                    msg = [server, PPP_HEARTBEAT]
                    backend.send_multipart(msg)
                heartbeat_at = time.time() + HEARTBEAT_INTERVAL
            
            """ backend.send(address, zmq.SNDMORE)
            backend.send(b"", zmq.SNDMORE)
            backend.send_string(LIST_REQUEST, zmq.SNDMORE)
            backend.send_string("Hello") """
        if socks.get(frontend) == zmq.POLLIN:
            frames = frontend.recv_multipart()
            if not frames:
                break
            address = frames[0]
            msg = frames[2:]
            """ 
            print("frames:")
            print(frames)
            print("address:")
            print(address)
            print("msg:")
            print(msg)
            """
            request=check_request(msg)
            if(request[0]==False):
                print("E: Invalid message from client: %s" % msg)
                continue
            elif request[0] == True:
                frontend.send(address, zmq.SNDMORE)
                frontend.send(b"", zmq.SNDMORE)
                frontend.send_string("alive")
            else:
                frames.insert(0, servers.next())
                backend.send_multipart(frames)
                
            


        servers.purge()


if __name__ == "__main__":
    
    if len(sys.argv) != 2 or sys.argv[1] not in ["0","1"]:
        print("Usage: python3 broker.py <argument>")
        sys.exit(1)

    arg_value = int(sys.argv[1])
    
    
    context = zmq.Context(1)
    print("Frontend: %s" % PROXYLIST[arg_value][0])
    print("Backend: %s" % PROXYLIST[arg_value][1])
    
    frontend = context.socket(zmq.ROUTER) # ROUTER
    backend = context.socket(zmq.ROUTER)  # ROUTER
    frontend.bind(PROXYLIST[arg_value][0]) # For clients
    backend.bind(PROXYLIST[arg_value][1])  # For servers

    poll_servers = zmq.Poller()
    poll_servers.register(backend, zmq.POLLIN)

    poll_both = zmq.Poller()
    poll_both.register(frontend, zmq.POLLIN)
    poll_both.register(backend, zmq.POLLIN)

    servers = ServerQueue()

    heartbeat_at = time.time() + HEARTBEAT_INTERVAL

    run()