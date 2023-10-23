import zmq
import json

"""
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


"""

def auth():
    global username
    global data
    while True:
        print(str(data["john_doe"]["password"]))

        username=input("Enter your username: ")
        password=input("Enter your password: ")
        
        # check the name and password
        if username in data:
            
            if password == data[username]["password"]:
                print("Authentication successful")
                break
            else:
                print("Wrong password")
        else:
            print("Authentication failed")


def display_list(list_id):
    global username
    global data
    print(f"Shopping list: {data[username]['lists'][list_id]['name']}")
    print("Items:")
    for item in data[username]["lists"][list_id]:
        if item != "name" and item != "lastUpdate":
            print(f"{item}: {data[username]['lists'][list_id][item]['quantity']}")

def edit_list(list_id):
    global username
    global data
    while True:
        # display the items
        display_list(list_id)

        action=input("Enter an action (add/delete/check/quit): ").lower()

        if action == "add":
            item=input("Enter an item to add: ")
            data[username]["lists"][list][item]={"quantity": 1, "bought": False}
            print("Item added")
        elif action == "delete":
            item=input("Enter an item to delete: ")
            if item in data[username]["lists"][list]:
                del data[username]["lists"][list][item]
                print("Item deleted")
            else:
                print("Item not found")
        elif action == "quit":
            break
        else:
            print("Invalid action")

def offline():
    global username
    global data
  
    # display the shopping lists
    print("Shopping lists:")
    for list_id in data[username]["lists"]:
        print(f"{list_id}: {data[username]['lists'][list_id]['name']}")

    while True:
        # ask for the list to edit
        list_id=input("Enter the list id to edit: ")

        # check if the list exists
        if list_id in data[username]["lists"]:
            print("List found")
            edit_list(list_id)
            break




if __name__ == "__main__":
    """ context = zmq.Context()
    client = context.socket(zmq.REQ)
    client.connect("tcp://127.0.0.1:5557") """

    data = None
    username = None
    # open the json file
    with open("./data/local/users.json", "r") as f:
        data = json.load(f)

    data = json.loads(data)

    # local
    auth()

    # stabilish connection with the server
    
    # offline mode
    offline()





""" timeout 2 seconds
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
        break     """

