from random import randint
import time

import zmq
import json
from AWORSet import AWORSet
import uuid

HEARTBEAT_LIVENESS = 3
HEARTBEAT_INTERVAL = 1
INTERVAL_INIT = 1
INTERVAL_MAX = 32

#  Paranoid Pirate Protocol constants
PPP_READY = b"\x01"      # Signals server is ready
PPP_HEARTBEAT = b"\x02"  # Signals server heartbeat

PROXYLIST=["tcp://127.0.0.1:5556","tcp://127.0.0.1:5558"]
MAX_RETRIES=3
TIMEOUT=3500 #milliseconds

def read_data():
    with open("./data/cloud/data.json", "r") as f:
        data = json.load(f)

    data = json.loads(data)
    lists=[]

    for key in data:
        aworset=AWORSet(data[key]["id"],data[key]["name"],data[key]["owner"])
        for item in data[key]["items"]:
            aworset.add(item,data[key]["items"][item]["quantity"],data[key]["items"][item]["bought"])
        
        lists.append(aworset)
    
    return lists



def server_socket(context, poller):
    """Helper function that returns a new configured socket
       connected to the Paranoid Pirate queue"""
    server = context.socket(zmq.DEALER) # DEALER
    identity = b"%04X-%04X" % (randint(0, 0x10000), randint(0, 0x10000))
    server.setsockopt(zmq.IDENTITY, identity)
    poller.register(server, zmq.POLLIN)
    for proxy in PROXYLIST:
        print(f"Trying to connect to {proxy}")
        server.connect(proxy)
        try:
            amountOfRetries = 0
            
            while amountOfRetries < MAX_RETRIES:
                server.send_multipart([b'ping'])
                
                auxPoller = zmq.Poller()
                auxPoller.register(server, zmq.POLLIN)

                # Wait for the specified timeout for a response
                socks = dict(auxPoller.poll(TIMEOUT))
                if server in socks and socks[server] == zmq.POLLIN:
                    # Receive reply from server
                    message = server.recv_multipart()
                    print(f"Received reply: {message}")
                    server.send(PPP_READY)
                    return server
                else:
                    print("Retrying to connect to the proxy")
                    server.close()
                    amountOfRetries += 1 
                    server= context.socket(zmq.DEALER)
                    server.setsockopt(zmq.IDENTITY, identity)
                    poller.register(server, zmq.POLLIN)
                    server.connect(proxy)
        except KeyboardInterrupt:
            break
        
    print("Max retries reached. Exiting...")
    return None



def run():
    global liveness
    global interval
    global heartbeat_at
    global server
    global context

    poller = zmq.Poller()
    server = server_socket(context, poller)
    if server is None:
        print("Could not connect to any proxy. Exiting...")
        return

    cycles = 0
    while True:
        socks = dict(poller.poll(HEARTBEAT_INTERVAL * 1000))

        # Handle server activity on backend
        if socks.get(server) == zmq.POLLIN:
            #  Get message
            #  - 3-part envelope + content -> request
            #  - 1-part HEARTBEAT -> heartbeat
            frames = server.recv_multipart()
            if not frames:
                break # Interrupted

            if len(frames) == 3:
                # Simulate various problems, after a few cycles
                cycles += 1
                if cycles > 3 and randint(0, 5) == 0:
                    print("I: Simulating a crash")
                    break
                if cycles > 3 and randint(0, 5) == 0:
                    print("I: Simulating CPU overload")
                    time.sleep(3)
                print("I: Normal reply")
                server.send_multipart(frames)
                liveness = HEARTBEAT_LIVENESS
                time.sleep(1)  # Do some heavy work
            elif len(frames) == 1 and frames[0] == PPP_HEARTBEAT:
                print("I: Queue heartbeat")
                liveness = HEARTBEAT_LIVENESS
            else:
                print("E: Invalid message: %s" % frames)
            interval = INTERVAL_INIT
        else:
            liveness -= 1
            if liveness == 0:
                print("W: Heartbeat failure, can't reach queue")
                print("W: Reconnecting in %0.2fs..." % interval)
                time.sleep(interval)

                if interval < INTERVAL_MAX:
                    interval *= 2
                poller.unregister(server)
                server.setsockopt(zmq.LINGER, 0)
                server.close()
                server = server_socket(context, poller)
                liveness = HEARTBEAT_LIVENESS
        if time.time() > heartbeat_at:
            heartbeat_at = time.time() + HEARTBEAT_INTERVAL
            print("I: server heartbeat")
            server.send(PPP_HEARTBEAT)
        

if __name__ == "__main__":
    data=read_data()
    
    context = zmq.Context(1)
    liveness = HEARTBEAT_LIVENESS
    interval = INTERVAL_INIT
    heartbeat_at = time.time() + HEARTBEAT_INTERVAL
    run()
    
    
    
    
    
    