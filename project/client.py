import zmq
import json
from utils import *
import uuid
PROXYLIST=["tcp://127.0.0.1:5555","tcp://127.0.0.1:5557"]
MAX_RETRIES=3
TIMEOUT=4500 #milliseconds

LIST_REQUEST=b"\x03" # Client sends this to Server to request a list
LIST_RESPONSE=b"\x04" # Server sends this to client with the list
LIST_UPDATE=b"\x05" # Client sends this to Server to update the list
LIST_UPDATE_RESPONSE=b"\x06" # Server sends this to client with the update status
LIST_DELETE=b"\x07" # Client sends this to Server to delete a list
LIST_DELETE_RESPONSE=b"\x08" # Server sends this to client with the delete status
LIST_CREATE=b"\x09" # Client sends this to Server to create a list
LIST_CREATE_RESPONSE=b"\x10" # Server sends this to client with the create status
LIST_DELETE_DENIED=b"\x11" # Server sends this to client when the list owner is not the client
LIST_RESPONSE_NOT_FOUND=b"\x12" # Server sends this to client when the list is not found
LIST_UPDATE_OFFLINE=b"\x13" # Client sends this to Server to update the list when offline

# Check the response from the server
def check_response(message_type):
    if message_type==LIST_RESPONSE:
        print("List found")
        return True
    elif message_type==LIST_UPDATE_RESPONSE:
        #print("List update")
        return True
    elif message_type==LIST_DELETE_RESPONSE:
        #print("List deleted")
        return True
    elif message_type==LIST_DELETE_DENIED:
        print("Not owner of the list")
        return True
    elif message_type==LIST_CREATE_RESPONSE:
        print("List created")
        return True
    elif message_type==LIST_RESPONSE_NOT_FOUND:
        print("List not found")
        return False

# Sends a request to the server
def send_message(action, message):
    global client
    global username
    global used_proxy
   
    if connectToProxy()==False:
        return None
    try:
        amountOfRetries = 0
        # Retry sending the message if no response is received
        while amountOfRetries < MAX_RETRIES:
            print("Sending message...")
            client.send(action, zmq.SNDMORE)  
            # If the action is LIST_DELETE, the username is  needed          
            if action==LIST_DELETE:
                client.send_string(username,zmq.SNDMORE)
            client.send_string(message)
            poller = zmq.Poller()
            poller.register(client, zmq.POLLIN)

            # Wait for the specified timeout for a response
            socks = dict(poller.poll(TIMEOUT))
            if client in socks and socks[client] == zmq.POLLIN:
                # Receive reply from server
                message = client.recv_multipart()
                response=check_response(message[0])
                print("message:",message[1])
                if response==False:
                    return "list not found"
                return message[1].decode("utf-8")
            else:
                print("Retrying to send message")
                amountOfRetries += 1    
                client.close()
                client= context.socket(zmq.REQ)
                client.connect(used_proxy) 
        
        if amountOfRetries==MAX_RETRIES:
            print("Max retries reached. Exiting...")
            return None  
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

# Display a list
def display_list(aworset):
    print("\n=====================================")
    print(f"Shopping list: {aworset.list_name}")
    aworset.lookup()
    print("=====================================\n")

# Edit a list
def edit_list(aworset):
     
    while True:
        # display the list information
        display_list(aworset)

        action=input("Enter an action (Add/Update/Remove/Quit): ").lower()

        # add an item
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
        
        # update an item
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
        
        # remove an item
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

# Offline mode edit list
def offline_edit():
    global username
    global data
    
    # display the shopping lists
    print("\n=====================================")
    print(data[username]['name'])
    print("Shopping lists:")
    for list_id in data[username]["lists"]:
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
            edit_list(aworset)
            
            print("Saving changes...")
            save_locally(list_id,aworset_to_json(aworset))
            print("Changes saved")
            inp=("Do you want to send the changes to the server? (y/n)")
            while inp != "y" and inp != "n":
                inp=input("Do you want to send the changes to the server? (y/n)").lower()
            
            if inp=="y":
                print("Sending changes to the server...")
                response=send_message(LIST_UPDATE_OFFLINE,aworset_to_json(aworset))
                print("Response:",response)
                if response!="updated":
                    print("Error sending list, try again at a later time")
                    
                
            
            break

# Offline mode create list
def offline_create():
    global username
    global data
    
    list_name=input("Enter list name: ")
    list_id=str(uuid.uuid4())
    print("List name:",list_name,"\nList id:",list_id)
    aworset=AWORSet(list_id,list_name,username)
    edit_list(aworset)
    print("Saving changes...")
    save_locally(list_id,aworset_to_json(aworset))
    
    
    inp=("Do you want to send the changes to the server? (y/n)")
    while inp != "y" and inp != "n":
        inp=input("Do you want to send the changes to the server? (y/n)").lower()
    
    if inp=="y":
        print("Sending changes to the server...")
        response=send_message(LIST_CREATE,aworset_to_json(aworset))
        print("Response:",response)
        if response!="created":
            print("Error sending list, try again at a later time")
        

# Offline mode
def offline():
    global username
    global data
  
    inp=input("Select an action: (create/edit) list or (quit): ").lower()
    
    while inp!="quit" or inp!="create" or inp!="edit":
        if inp=="quit":
            break
        elif inp=="create":
            offline_create()
        elif inp=="edit":
            offline_edit()
        else:
            print("Invalid action")
        inp=input("Select an action: (create/edit) list or (quit): ").lower()
    

# Connects to a proxy
def connectToProxy():
    global context
    global client
    global used_proxy
    poller = zmq.Poller()
    # Try to connect to the first proxy available
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
                    used_proxy=proxy
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

# Online mode
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
    global data
    list_id=input("Enter list id to delete: ")
    response=send_message(LIST_REQUEST,list_id)
    print("Response:",response)
    while response=="list not found":
        list_id=input("Enter list id:")
        response=send_message(LIST_REQUEST,list_id)

    if response==None:
        return
    
    response=send_message(LIST_DELETE,list_id)
    print("Response:",response)
    
    if response!="deleted":
        if response=="denied":
            print("You are not the owner of the list")
            return
        return
    print("Deleting list locally...")
    
    with open("./data/local/users.json", "r") as f:
        data = json.load(f)
    
    data = json.loads(data)
    del data[username]["lists"][list_id]
    json_data = json.dumps(data)
    with open("./data/local/users.json", "w") as f:
        json.dump(json_data, f, indent=2)
    
    
    
# Create a new list
def create_list():
    global username
    global client
    
    list_name=input("Enter list name: ")
    list_id=str(uuid.uuid4())
    print("List id:",list_id)   
    aworset=AWORSet(list_id,list_name,username)
    edit_list(aworset)
    print("Saving changes...")
    save_locally(list_id,aworset_to_json(aworset))
    print("Changes saved locally. Sending changes to the server...")
    response=send_message(LIST_CREATE,aworset_to_json(aworset))
    print("Response:",response)
    if response!="created":
        print("Error creating list, try again at a later time")
        
# Online mode edit list
def list_edit():
    global username
    global client
    
    list_id=input("Enter list id:")
    
    response=send_message(LIST_REQUEST,list_id)
    # check if the list exists
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
    aworset.lookup()
    print("Saving changes...")
    save_locally(list_id,aworset_to_json(aworset))
    print("Changes saved locally. Sending changes to the server...")
    response=send_message(LIST_UPDATE,aworset_to_json(aworset))
    print("Response:",response)
    
        
    
    
def initial_interface():
    inp=input("Connect to server or use offline mode? (online/offline): ").lower()
    while inp!="online" or inp!="offline":
        if inp=="online":
            online()
        elif inp=="offline":
            offline()
        else:
            print("Invalid action")
        inp=input("Connect to server or use offline mode? (online/offline): ").lower()
        
        
    

if __name__ == "__main__":
    data = None
    username = None
    context = zmq.Context()
    client = context.socket(zmq.REQ)
    used_proxy = None
    # Reads the initial data
    with open("./data/local/users.json", "r") as f:
        data = json.load(f)

    data = json.loads(data)
   
    # Authentication
    auth()
    # Initial interface
    initial_interface()
    
    



