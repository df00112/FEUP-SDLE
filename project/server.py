import zmq

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
