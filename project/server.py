from random import randint
import time
import sys
import zmq
import json
from AWORSet import AWORSet
import uuid
from utils import *

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

LIST_REQUEST=b"\x03" # Client sends this to broker to request a list
LIST_RESPONSE=b"\x04" # Broker sends this to client with the list
LIST_UPDATE=b"\x05" # Client sends this to broker to update the list
LIST_UPDATE_RESPONSE=b"\x06" # Broker sends this to client with the update status
LIST_DELETE=b"\x07" # Client sends this to broker to delete a list
LIST_DELETE_RESPONSE=b"\x08" # Broker sends this to client with the delete status
LIST_CREATE=b"\x09" # Client sends this to broker to create a list
LIST_CREATE_RESPONSE=b"\x10" # Broker sends this to client with the create status
LIST_DELETE_DENIED=b"\x11" # Broker sends this to client when the list owner is not the client
LIST_RESPONSE_NOT_FOUND=b"\x12" # Broker sends this to client when the list is not found

PUB_LIST = ["tcp://*:6000", "tcp://*:6001", "tcp://*:6002"]
SUB_LIST = ["tcp://localhost:6000", "tcp://localhost:6001", "tcp://localhost:6002"]

def read_data():
    with open("./data/cloud/data.json", "r") as f:
        json_data = json.load(f)

    data = json_data
    lists=[]
    for lst in data:
        aux=json.loads(lst)
        aworset=json_to_aworset(aux)
        lists.append(aworset)
    
    return lists

def update_database(aworset):
    with open("./data/cloud/data.json", "r") as f:
        json_data = json.load(f)
        
    index_to_update = None
    list_id=aworset.list_id
    
    for i, item in enumerate(json_data):
        aux=json.loads(item)
        if "list_id" in item and aux["list_id"] == list_id:
            index_to_update = i
            break
    
    if index_to_update is not None:
        # Update the data for the specific list
        json_data[index_to_update] = aworset_to_json(aworset)
        with open("./data/cloud/data.json", "w") as f:
            json.dump(json_data, f, indent=2)
    else:
        # The list does not exist in the database
        # remove it from the server
        data.remove(aworset)

def create_list_database(aworset):
    with open("./data/cloud/data.json", "r") as f:
        json_data = json.load(f)
        
    index_to_update = None
    list_id=aworset.list_id
    
    for i, item in enumerate(json_data):
        aux=json.loads(item)
        if "list_id" in item and aux["list_id"] == list_id:
            index_to_update = i
            break
    
    if index_to_update is None:
        json_data.append(aworset_to_json(aworset))
        with open("./data/cloud/data.json", "w") as f:
            json.dump(json_data, f, indent=2)

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

def send_to_all(msg):
    global sub_sockets
    for sub_socket in sub_sockets:
        print("Sending to socket")
        print(msg)

def list_request(msg):
    global data
    print("IN LIST REQUEST")
    print(msg[1])
    list_id=msg[1].decode("utf-8")
    print(list_id)
    for aworset in data:
        if aworset.list_id==list_id:
            return [LIST_RESPONSE,aworset_to_json(aworset)]
    return [LIST_RESPONSE_NOT_FOUND,"not found"]


def list_update(msg):
    global data
    aworset=json_to_aworset(msg[2])
    temp=None
    for awor in data:
        if awor.list_id==aworset.list_id:
            awor.join(aworset)
            temp=awor
            break
        
    update_database(temp)
    return [LIST_UPDATE_RESPONSE,"updated"]

def list_delete(msg):
    global data
    # msg = [LIST_DELETE, list_id, userID]
    list_id=msg[1] # testar
    user=msg[2] # testar

    for awor in data:
        if awor.list_id==list_id:
            if awor.owner!=user:
                return [LIST_DELETE_DENIED, "denied"]
            else:
                data.remove(awor)
                return [LIST_DELETE_RESPONSE,"deleted"]
    
    return # Testar em baixo depois
    
        
    with open("./data/cloud/data.json", "r") as f:
        json_data = json.load(f)
        
    index_to_delete = None
    
    for i, item in enumerate(json_data):
        aux=json.loads(item)
        if "list_id" in item and aux["list_id"] == aworset.list_id:
            index_to_delete = i
            break
    
    if index_to_delete is not None:
        # Delete the list
        del json_data[index_to_delete]

        # Write the updated data back to the file
        with open("./data/cloud/data.json", "w") as f:
            json.dump(json_data, f, indent=2)
        return [LIST_DELETE_RESPONSE]
   
def list_create(msg):
    global data
    aworset=json_to_aworset(msg[1])
    data.append(aworset)
    create_list_database(aworset)
    return [LIST_CREATE_RESPONSE,"created"]

def handle_request(msg):
    request_type=msg[0]
    print(f"Request type: {request_type}")
    if request_type == LIST_REQUEST:
        print("IN LIST REQUEST")
        return list_request(msg)
    elif request_type == LIST_UPDATE:
        return list_update(msg)
    elif request_type == LIST_DELETE:
        return list_delete(msg)
    elif request_type == LIST_CREATE:
        return list_create(msg) 
    else:
        return [None, None]

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
            print(f"Received message: {frames}")
            if not frames:
                break # Interrupted

            if len(frames) == 4:
                print("Frames: ",frames)
                response=handle_request(frames[2:])
                server.send(frames[0],zmq.SNDMORE)
                server.send(response[0],zmq.SNDMORE)
                server.send_string(response[1])
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
    if len(sys.argv) != 2 or sys.argv[1] not in ["0","1"]:
        print("Usage: python3 broker.py <argument>")
        sys.exit(1)

    arg_value = int(sys.argv[1])

    data=read_data()
    
    context = zmq.Context(1)

    pub_context = zmq.Context(1)
    pub_socket = pub_context.socket(zmq.PUB)
    print("PUB: %s" % PUB_LIST[arg_value])
    pub_socket.bind(PUB_LIST[arg_value])

    sub_sockets = []
    for i in range(len(PUB_LIST)):
        if i == arg_value:
            continue
        else:
            sub_context = zmq.Context(1)
            sub_socket = sub_context.socket(zmq.SUB)
            sub_socket.connect(SUB_LIST[i])
            sub_socket.setsockopt(zmq.SUBSCRIBE, b"")
            sub_sockets.append(sub_socket)

    liveness = HEARTBEAT_LIVENESS
    interval = INTERVAL_INIT
    heartbeat_at = time.time() + HEARTBEAT_INTERVAL
    run()
    
    
    
    
    
    