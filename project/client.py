import zmq
import json
import datetime
import pytz
from utils import *
import uuid
PROXYLIST=["tcp://127.0.0.1:5555","tcp://127.0.0.1:5557"]
MAX_RETRIES=3
TIMEOUT=4500 #milliseconds

LIST_REQUEST=b"\x03" # Client sends this to broker to request a list
LIST_RESPONSE=b"\x04" # Broker sends this to client with the list
LIST_UPDATE=b"\x05" # Client sends this to broker to update the list
LIST_UPDATE_RESPONSE=b"\x06" # Broker sends this to client with the update status
LIST_DELETE=b"\x07" # Client sends this to broker to delete a list
LIST_DELETE_RESPONSE=b"\x08" # Broker sends this to client with the delete status
LIST_CREATE=b"\x09" # Client sends this to broker to create a list
LIST_CREATE_RESPONSE=b"\x10" # Broker sends this to client with the create status
LIST_DELETE_DENIED=b"\x11" # Broker sends this to client when the list owner is not the client

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
def check_response(message_type):
    if message_type==LIST_RESPONSE:
        print("List found")
        return True
    elif message_type==LIST_UPDATE_RESPONSE:
        print("List updated")
        return True
    elif message_type==LIST_DELETE_RESPONSE:
        print("List deleted")
        return True
    elif message_type==LIST_DELETE_DENIED:
        print("Not owner of the list")
        return False
    elif message_type==LIST_CREATE_RESPONSE:
        print("List created")
        return True
    else:
        print("List not found")
        return False

def send_message(action, message):
    global client
    global username
    print("MESSAGE: ",message)
    if connectToProxy()==False:
        return None
    try:
        amountOfRetries = 0
        
        while amountOfRetries < MAX_RETRIES:
            print("Sending message...")
            client.send(action, zmq.SNDMORE)            
            if action==LIST_DELETE:
                client.send_string(username,zmq.SNDMORE)
            client.send_string(message)
            print("message sent: ",message)
            poller = zmq.Poller()
            poller.register(client, zmq.POLLIN)

            # Wait for the specified timeout for a response
            socks = dict(poller.poll(TIMEOUT))
            if client in socks and socks[client] == zmq.POLLIN:
                print("hAHAHAHAH")
                # Receive reply from server
                message = client.recv_multipart()
                print("message received: ",message)
                response=check_response(message[0])
                if response==False:
                    return "list not found"
                return message[1]
            else:
                print("Retrying to send message")
                amountOfRetries += 1       
    except KeyboardInterrupt:
        return None



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

def edit_list(aworset):
     
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
        print(list_name,":", list_id)
    while True:
        # ask for the list to edit
        list_id=input("Enter the list id to edit: ")

        # check if the list exists
        if list_id in data[username]["lists"]:
            print("List found")
            list_info  = json.loads(data[username]['lists'][list_id])
            aworset=json_to_aworset(list_info)
            lst=edit_list(aworset)
            
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
                    message = message[0].decode("utf-8")
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

def online():
    global client
    global username
    
    resp=input("Select an action: (create/edit/delete) list from servers or (quit): ").lower()
    while resp!="quit" or resp!="create" or resp!="edit" or resp!="delete":
        if resp=="quit":
            break
        elif resp=="create":
            create_list()
        elif resp=="edit":
            list_edit()
        elif resp=="delete":
            delete_list()
        else:
            print("Invalid action")
        resp=input("Select an action: (create/edit/delete) list from servers or (quit): ").lower()

def delete_list():
    global username
    global client
    
    list_id=input("Enter list id to delete: ")
    response=send_message(LIST_REQUEST,list_id)
    while response=="list not found":
        list_id=input("Enter list id:")
        response=send_message(LIST_REQUEST,list_id)

    if response==None:
        return
    
    response=send_message(LIST_DELETE,list_id)
    while response=="list not found":
        response=send_message(LIST_DELETE,list_id)
    
    print("Deleting list locally...")
    
    with open("./data/local/users.json", "r") as f:
        data = json.load(f)
    
    data = json.loads(data)
    del data[username]["lists"][list_id]
    json_data = json.dumps(data)
    with open("./data/local/users.json", "w") as f:
        json.dump(json_data, f, indent=2)
    

def create_list():
    global username
    global client
    
    list_name=input("Enter list name: ")
    list_id=uuid.uuid4()
    aworset=AWORSet(list_name,list_id,username)
    edit_list(aworset)
    print("Saving changes...")
    save_locally(list_id,aworset_to_json(aworset))
    print("Changes saved locally. Sending changes to the server...")
    response=send_message(LIST_CREATE,aworset_to_json(aworset))
    if response!="list created":
        print("Error creating list, try again at a later time")
        
    
def list_edit():
    global username
    global client
    
    list_id=input("Enter list id:")
    
    response=send_message(LIST_REQUEST,list_id)
    
    while response=="list not found":
        list_id=input("Enter list id:")
        response=send_message(LIST_REQUEST,list_id)
    
    if response==None:
        return
    
    print("Response:",response)
    response=json.loads(response)
    print("New response:",response)
    aworset=json_to_aworset(response)
    edit_list(aworset)
    print("Saving changes...")
    save_locally(list_id,aworset_to_json(aworset))
    print("Changes saved locally. Sending changes to the server...")
    send_message(LIST_UPDATE,aworset_to_json(aworset))

    
        
    

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
    auth()
    
    # stabilish connection with the server
    if(connectToProxy()):
        online()
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

