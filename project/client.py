import zmq
import json
import datetime
import pytz
from utils import *

PROXYLIST=["tcp://127.0.0.1:5555","tcp://127.0.0.1:5557"]
MAX_RETRIES=3
TIMEOUT=3500 #milliseconds



"""
def receive_messages():
    while True:
        update_message = subscriber.recv_string()
        print(f"Received update: {update_message}")
        
        

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


def display_list(aworset):
    print("\n=====================================")
    print(f"Shopping list: {aworset.list_name}")
    aworset.lookup()
    print("=====================================\n")

def edit_list(lst):
    
    aworset=json_to_aworset(lst)
    
    while True:
        # display the items
        display_list(aworset)

        action=input("Enter an action (Add/Update/Remove/Quit): ").lower()

        if action == "add":
            item=input("Enter a new item to add: ")
            while item in aworset.get_items_names():
                print("Item already exists")
                item=input("Enter a new item to add: ")
            quantity=input("Enter the quantity: ")
            while not quantity.isnumeric():
                print("Invalid quantity")
                quantity=input("Enter the quantity: ")
            aworset.add_new(item,int(quantity),0)
            print("Item added")
            
        elif action == "update":
            item=input("Enter an item to update: ")
            while item not in aworset.get_items_names():
                print("Item doens't exists")
                item=input("Enter a item to update: ")
                
            quantity=input("Enter the quantity: ")
            while not quantity.isnumeric():
                print("Invalid quantity")
                quantity=input("Enter the quantity: ")
            
            bought=input("Enter the status (bought/not bought): ").lower()
            while bought != "bought" and bought != "not bought":
                print("Invalid status")
                bought=input("Enter the status (bought/not bought): ").lower()
            
            bought= 0 if bought == "not bought" else 1
            aworset.update_item_quantity(item,int(quantity))
            aworset.update_item_status(item,bought)
            
            print("Item updated")
        
        elif action == "remove":
            item=input("Enter an item to remove: ")
            while item not in aworset.get_items_names():
                print("Item doens't exists")
                item=input("Enter a item to remove: ")
            aworset.remove(item)
            print("Item removed")
            
        elif action == "quit":
            break
        else:
            print("Invalid action")
    

    return aworset_to_json(aworset)

def save_locally(list_id, listToBeSaved):
    global username
    global data
    
    with open("./data/local/users.json", "r") as f:
        data = json.load(f)

    data = json.loads(data)
    
    # save the list locally
    data[username]["lists"][list_id] = listToBeSaved

    json_data = json.dumps(data)
    with open("./data/local/users.json", "w") as f:
        json.dump(json_data, f, indent=2)

def offline():
    global username
    global data
  
    # display the shopping lists
    print("\n=====================================")
    print(data[username]['name'])
    list_keys = list(data[username]["lists"].keys())
    print(f"Shopping lists: {list_keys}")
    print("Shopping lists:")
    for list_id in data[username]["lists"]:
        #print(data[username]['lists'][list_id])
        list_info  = json.loads(data[username]['lists'][list_id])

        list_name = list_info ['list_name']
        print(list_name)
        #print(f"{list_id}: {data[username]['lists'][list_id]['list_name']} ")
        #print(f"{list_id}: {list_name} ")
        #print(f"{list_id}: {data[username]['lists'][list_id]['list_name']} ")
        #print(f"{list_id}: {data[username]['lists'][list_id]['list_name']} ")

    while True:
        # ask for the list to edit
        list_id=input("Enter the list id to edit: ")

        # check if the list exists
        if list_id in data[username]["lists"]:
            print("List found")
            list_info  = json.loads(data[username]['lists'][list_id])
            lst=edit_list(list_info)
            
            print("Saving changes...")
            save_locally(list_id,lst)
            print("Changes saved")
            print("Do you want to send the changes to the server? (y/n)")
            
            break


def connectToProxy():
    global context
    global client
    poller = zmq.Poller()
    for proxy in PROXYLIST:
        print(f"Trying to connect to {proxy}")
        client= context.socket(zmq.REQ)
        client.connect(proxy)
        try:
            amountOfRetries = 0
            
            while amountOfRetries < MAX_RETRIES:
                client.send_multipart([b'ping'])
                
                poller.register(client, zmq.POLLIN)
                poller = zmq.Poller()
                poller.register(client, zmq.POLLIN)

                # Wait for the specified timeout for a response
                socks = dict(poller.poll(TIMEOUT))
                if client in socks and socks[client] == zmq.POLLIN:
                    # Receive reply from server
                    message = client.recv_multipart()
                    print(f"Received reply: {message}")
                    return True
                else:
                    print("Retrying to connect to the proxy")
                    client.close()
                    amountOfRetries += 1 
                    client= context.socket(zmq.REQ)
                    client.connect(proxy)           
        except KeyboardInterrupt:
            break
    print("Max retries reached. Exiting...")
    return False
    

if __name__ == "__main__":
    data = None
    username = None
    context = zmq.Context()
    client = context.socket(zmq.REQ)
    # open the json file
    with open("./data/local/users.json", "r") as f:
        data = json.load(f)

    data = json.loads(data)
    username="john_doe"
    # local
    #auth()
    offline()
    exit()
    # stabilish connection with the server
    if(connectToProxy()):
        print("Connected to a proxy")
        # online mode
        #online()
    else:
        exit()
        print("No proxy available")
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

