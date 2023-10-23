import zmq
import threading

def receive_messages():
    while True:
        update_message = subscriber.recv_string()
        print(f"Received update: {update_message}")
        

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://127.0.0.1:5556")

client = context.socket(zmq.REQ)
client.connect("tcp://127.0.0.1:5557")

# Subscribe to shopping list updates
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")


# Start a thread to receive messages in the background
receiver_thread = threading.Thread(target=receive_messages)
receiver_thread.daemon = True
receiver_thread.start()


while True:
    try:
        action = input("Enter an action (add/delete/quit): ").lower()

        if action == "add":
            item = input("Enter an item to add: ")
            client.send_json({"action": "add", "item": item})
            response = client.recv_json()
            print(response["status"])

        elif action == "delete":
            item = input("Enter an item to delete: ")
            client.send_json({"action": "delete", "item": item})
            response = client.recv_json()
            print(response["status"])

        elif action == "quit":
            break

        

    except KeyboardInterrupt:
        break

subscriber.close()
client.close()
context.term()


def auth():
    
    
    poller = zmq.Poller()
    poller.register(client, zmq.POLLIN)
    while True:
        name=input("Enter your name: ")
        password=input("Enter your password: ")
        
        client.send_string(f"{name}|{password}")
        socks=dict(poller.poll(2000))
        if socks:
            if socks.get(client) == zmq.POLLIN:
                message = client.recv_string(zmq.NOBLOCK)
                print(message)
                if message=="Authentication successful":
                    break
        else:    
            print("error: Server is not online")
            break    

if __name__ == "__main__":
    context = zmq.Context()
    client = context.socket(zmq.REQ)
    client.connect("tcp://127.0.0.1:5557")
    

    auth()
    
    
    