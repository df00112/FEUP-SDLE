from random import randint
import time
import sys
import zmq
import json
from AWORSet import AWORSet
import uuid
from utils import *
import threading

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
REREAD_DATABASE=b"\x12"
LIST_UPDATE_OFFLINE=b"\x13" # Client sends this to broker to update a list in offline mode

PUB_LIST = ["tcp://*:6000", "tcp://*:6001", "tcp://*:6002"]
SUB_LIST = ["tcp://localhost:6000", "tcp://localhost:6001", "tcp://localhost:6002"]

class ZmqSubscriberThread(threading.Thread):
    def __init__(self, sub_sockets, global_data, data_lock):
        super(ZmqSubscriberThread, self).__init__()
        self.sub_sockets = sub_sockets
        self.global_data = global_data
        self.data_lock = data_lock
        self.stop_requested = False
    def stop(self):
        self.stop_requested = True
    def run(self):
        poller = zmq.Poller()

        # Add each socket to the poller with the events you want to monitor (e.g., zmq.POLLIN)
        for socket in self.sub_sockets:
            poller.register(socket, zmq.POLLIN)

        try:
            while not self.stop_requested:
                # Poll with no timeout
                socks = dict(poller.poll())
                if self.stop_requested:
                    break
                # See if a sub_socket is receiving a message
                if socks:
                    for sub_socket in self.sub_sockets:
                        if sub_socket in socks and socks[sub_socket] == zmq.POLLIN:
                            # Receive message from publisher

                            # Access and modify the global variable with a lock
                            with self.data_lock:
                                message = sub_socket.recv_multipart() 
                                request=message[0]
                                print("PUB MESSAGE: ",message[0])
                                print("PUB REQUEST: ",request)
                                if request==LIST_CREATE:
                                    print("PUB LIST CREATE")
                                    message=json.loads(message[1].decode("utf-8"))
                                    aworset=json_to_aworset(message)
                                    aworset.lookup()
                                    self.global_data.append(aworset)
                                elif request==LIST_UPDATE:
                                    print("PUB LIST UPDATE")
                                    lst=json.loads(message[1])
                                    aworset=json_to_aworset(lst)
                                    for awor in self.global_data:
                                        if awor.list_id==aworset.list_id:
                                            awor.join(aworset)                                            
                                            break
                                elif request==LIST_DELETE:
                                    print("PUB LIST DELETE")
                                    list_id=message[2].encode('utf-8')
                                    for awor in self.global_data:
                                        if awor.list_id==list_id:
                                            self.global_data.remove(awor)
                                            break
                                
                                for awor in self.global_data:
                                    print("LIST ID: ",awor.list_id)
                               

                            break
                else:
                    print("No message received")

        except KeyboardInterrupt:
            return




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

def update_database(aworset,offlineMode=False):
    with open("./data/cloud/data.json", "r") as f:
        json_data = json.load(f)
        
    index_to_update = None
    aworset.lookup()
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
        print("OFFLINE MODE: ",offlineMode)
        if not offlineMode:
            # The list does not exist in the database
            # remove it from the server
            data.remove(aworset)
        else:
            data.append(aworset)
            create_list_database(aworset)

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
                    poller.register(server, zmq.POLLIN)
                    server.send(PPP_READY)
                    return server
                else:
                    print("Retrying to connect to the proxy")
                    server.close()
                    amountOfRetries += 1 
                    server= context.socket(zmq.DEALER)
                    server.setsockopt(zmq.IDENTITY, identity)
                    server.connect(proxy)
        except KeyboardInterrupt:
            break
        
    print("Max retries reached. Exiting...")
    return None


def list_request(msg):
    global data
    print("IN LIST REQUEST")
    print(msg[1])
    list_id=msg[1].decode("utf-8")
    print(list_id)
    with data_lock:
        for aworset in data:
            if aworset.list_id==list_id:
                return [LIST_RESPONSE,aworset_to_json(aworset)]
    return [LIST_RESPONSE_NOT_FOUND,"not found"]


def list_update(msg):
    global data
    global pub_socket
    print("IN LIST UPDATE")
    print("MSG: ",msg)
    lst=json.loads(msg[1])
    aworset=json_to_aworset(lst)
    temp=None
    with data_lock:
        for awor in data:
            if awor.list_id==aworset.list_id:
                awor.join(aworset)
                temp=awor
                break
            
    # That means that its from the offline mode
    if temp is None:
        temp=aworset
    offlineMode=False if msg[0]==LIST_UPDATE else True 
           
    update_database(temp,offlineMode)
    pub_socket.send(LIST_UPDATE,zmq.SNDMORE)
    pub_socket.send_string(aworset_to_json(aworset))

    return [LIST_UPDATE_RESPONSE,"updated"]

def list_delete(msg):
    global data
    global pub_socket
    # msg = [LIST_DELETE, list_id, userID]
    print("IN LIST DELETE")
    print("MSG: ",msg)
    list_id=msg[2].decode('utf-8') # testar
    user=msg[1].decode('utf-8') # testar
    print("LIST ID: ",list_id)
    print("USER: ",user)
    with data_lock:
        for awor in data:
            if awor.list_id==list_id:
                if awor.owner!=user:
                    return [LIST_DELETE_DENIED, "denied"]
                else:
                    data.remove(awor)
        
    
        
    with open("./data/cloud/data.json", "r") as f:
        json_data = json.load(f)
        
    index_to_delete = None
    
    for i, item in enumerate(json_data):
        aux=json.loads(item)
        if "list_id" in item and aux["list_id"] == list_id:
            index_to_delete = i
            break
    
    if index_to_delete is not None:
        # Delete the list
        del json_data[index_to_delete]

        # Write the updated data back to the file
        with open("./data/cloud/data.json", "w") as f:
            json.dump(json_data, f, indent=2)
        
        pub_socket.send(LIST_DELETE,zmq.SNDMORE)
        pub_socket.send_string(list_id)
        
        return [LIST_DELETE_RESPONSE,"deleted"]
   
def list_create(msg):
    global data
    global pub_socket
    global data_lock
    message=json.loads(msg[1])
    aworset=json_to_aworset(message)
    with data_lock:
        data.append(aworset)
    create_list_database(aworset)
    for awor in data:
        print("LIST ID: ",awor.list_id)
    
    pub_socket.send(LIST_CREATE,zmq.SNDMORE)
    pub_socket.send_string(aworset_to_json(aworset))
    return [LIST_CREATE_RESPONSE,"created"]

def handle_request(msg):
    request_type=msg[0]
    print(f"Request type: {request_type}")
    if request_type == LIST_REQUEST:
        print("IN LIST REQUEST")
        return list_request(msg)
    elif request_type == LIST_UPDATE or request_type == LIST_UPDATE_OFFLINE:
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
            #print(f"Received message: {frames}")
            if not frames:
                break # Interrupted
            #print("Frame size: ",len(frames))
            if (len(frames) == 4) or (len(frames) == 5):
                print("Frames: ",frames)
                response=handle_request(frames[2:])
                print("Response: ",response)
                server.send(frames[0],zmq.SNDMORE)
                server.send(response[0],zmq.SNDMORE)
                server.send_string(response[1])
            elif len(frames) == 1 :
                if frames[0] == PPP_HEARTBEAT:
                    #print("I: Queue heartbeat")
                    liveness = HEARTBEAT_LIVENESS
                elif frames[0]== REREAD_DATABASE:
                    print("REREAD DATABASE")
                    data=read_data()
                    print("DATA: ",data)
                    print("DATA LEN: ",len(data))
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
            #print("I: server heartbeat")
            server.send(PPP_HEARTBEAT)
        

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["0","1","2"]:
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

    
    data_lock=threading.Lock()
    subscriber_thread = ZmqSubscriberThread(sub_sockets, data, data_lock)
    subscriber_thread.start()
  
            
    liveness = HEARTBEAT_LIVENESS
    interval = INTERVAL_INIT
    heartbeat_at = time.time() + HEARTBEAT_INTERVAL
    try:
        run()
        
        
        
    except KeyboardInterrupt:
        
        subscriber_thread.stop()
        
        print("W: interrupt received, killing server...")
        sys.exit()
    
    
    