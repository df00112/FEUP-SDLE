from random import randint
import time
import json
import zmq

HEARTBEAT_LIVENESS = 3
HEARTBEAT_INTERVAL = 1
INTERVAL_INIT = 1
INTERVAL_MAX = 32

#  Paranoid Pirate Protocol constants
PPP_READY = b"\x01"      # Signals worker is ready
PPP_HEARTBEAT = b"\x02"  # Signals worker heartbeat

def worker_socket(context, poller):
    """Helper function that returns a new configured socket
       connected to the Paranoid Pirate queue"""
    identity = b"%04X-%04X" % (randint(0, 0x10000), randint(0, 0x10000))
    worker.setsockopt(zmq.IDENTITY, identity)
    poller.register(worker, zmq.POLLIN)
    worker.connect("tcp://localhost:5556")
    worker.send(PPP_READY)
    return worker

def get_list(list_name):
    with open ("./data/cloud/data.json", "r") as f:
        data = json.load(f)
    data = json.loads(data)
    
    for list in data:
        if list == list_name:
            return list
        
    return None


context = zmq.Context(1)
poller = zmq.Poller()

liveness = HEARTBEAT_LIVENESS
interval = INTERVAL_INIT

heartbeat_at = time.time() + HEARTBEAT_INTERVAL

worker = worker_socket(context, poller)
cycles = 0
while True:
    socks = dict(poller.poll(HEARTBEAT_INTERVAL * 1000))

    # Handle worker activity on backend
    if socks.get(worker) == zmq.POLLIN:
        #  Get message
        #  - 3-part envelope + content -> request
        #  - 1-part HEARTBEAT -> heartbeat
        frames = worker.recv_multipart()

        if not frames:
            break # Interrupted

        if len(frames) == 3:
            print("I: Normal reply")

            operation_type = frames[0].decode()
            client_name = frames[1].decode()
            data_json = frames[2].decode()

            list_data = json.loads(data_json)
            if operation_type == "create":
                print("Creating list")
            elif operation_type == "update":
                print("Updating list")
                # function to get the list from the json file
                cloud_data = get_list(list_data)
                #compare the last update date
                for list in cloud_data:
                    if list["name"] == list_data["name"]:
                        if list["lastUpdate"] < list_data["lastUpdate"]:
                            list["lastUpdate"] = list_data["lastUpdate"]
                            list["items"] = list_data["items"]
                            print("List updated")
                            # save the list to the json file
                            with open("./data/cloud/data.json", "w") as f:
                                json.dump(cloud_data, f)
                                print("List saved")
                        else:
                            print("List is already updated")

            elif operation_type == "delete":
                

            worker.send_multipart(frames)
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
            poller.unregister(worker)
            worker.setsockopt(zmq.LINGER, 0)
            worker.close()
            worker = worker_socket(context, poller)
            liveness = HEARTBEAT_LIVENESS
    if time.time() > heartbeat_at:
        heartbeat_at = time.time() + HEARTBEAT_INTERVAL
        print("I: Worker heartbeat")
        worker.send(PPP_HEARTBEAT)





""" import zmq

context = zmq.Context()

# publisher socket handles the server's heartbeats
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://127.0.0.1:5556")

# rep socket handles the main server-client communication - authentication, retrieve sub server
server = context.socket(zmq.REP)
server.bind("tcp://127.0.0.1:5557")

shopping_list = []

while True:
    try:
        # Handle client edit requests using REQ-REP
        edit_request = server.recv_json()
        
        action = edit_request["action"]
        item = edit_request.get("item")

        if action == "add":
            if item:
                shopping_list.append(item)
                update_message = f"Item added: {item}"
                publisher.send_string(update_message)

        elif action == "delete":
            if item in shopping_list:
                shopping_list.remove(item)
                update_message = f"Item deleted: {item}"
                publisher.send_string(update_message)

        elif action == "authentication":
            
            

    except KeyboardInterrupt:
        break

publisher.close()
server.close()
context.term()
 """