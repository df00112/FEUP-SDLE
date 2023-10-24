import zmq
import json
import datetime
import pytz
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


def display_list(list):
    print("\n=====================================")
    print(f"Shopping list: {list['name']}")
    print("Items:")
    for item in list:
        if item != "name" and item != "lastUpdate":
            print(f"{item}: {list[item]['quantity']} {'(bought)' if list[item]['bought'] == True else ''}")
    print("=====================================\n")

def edit_list(list):
    while True:
        # display the items
        display_list(list)

        action=input("Enter an action (Add/Update/Remove/Status/Quit): ").lower()

        if action == "add":
            item=input("Enter a new item to add: ")
            while item in list:
                print("Item already exists")
                item=input("Enter a new item to add: ")
            quantity=input("Enter the quantity: ")
            while not quantity.isnumeric():
                print("Invalid quantity")
                quantity=input("Enter the quantity: ")
            list[item]={"quantity": int(quantity), "bought": False}
            print("Item added")
            
        elif action == "update":
            item=input("Enter an item to update: ")
            while item not in list:
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
            list[item]={"quantity": int(quantity), "bought": True if bought == "bought" else False}
            
            print("Item updated")
        
        elif action == "remove":
            item=input("Enter an item to remove: ")
            while item not in list:
                print("Item doens't exists")
                item=input("Enter a item to remove: ")
            del list[item]
            print("Item removed")
            
        elif action == "status":
            item=input("Enter an item to check the status: ")
            while item not in list:
                print("Item doens't exists")
                item=input("Enter a item to check the status: ")
            bought=input("Enter the status (bought/not bought): ").lower()
            while bought != "bought" and bought != "not bought":
                print("Invalid status")
                bought=input("Enter the status (bought/not bought): ").lower()
                
            # update the bought field
            list[item]["bought"] = True if bought == "bought" else False
            
            print("The status was updated")
            
        elif action == "quit":
            break
        else:
            print("Invalid action")
    
    #update timestamp
    list["lastUpdate"] = datetime.datetime.now(pytz.timezone("Europe/Lisbon")).strftime("%Y-%m-%d %H:%M:%S")  
    
    return list

def save_locally(list_id,list):
    global username
    global data
    # save the list locally
    data[username]["lists"][list_id] = list

    json_data = json.dumps(data)
    with open("./data/local/users.json", "w") as f:
        json.dump(json_data, f, indent=4)

def offline():
    global username
    global data
  
    # display the shopping lists
    print("\n=====================================")
    list_keys = list(data[username]["lists"].keys())
    print(f"Shopping lists: {list_keys}")
    print("Shopping lists:")
    for list_id in data[username]["lists"]:
        print(f"{list_id}: {data[username]['lists'][list_id]['name']} (Last Update: {data[username]['lists'][list_id]['lastUpdate']})")

    while True:
        # ask for the list to edit
        list_id=input("Enter the list id to edit: ")

        # check if the list exists
        if list_id in data[username]["lists"]:
            print("List found")
            list=edit_list(data[username]["lists"][list_id])
            
            print("Saving changes...")
            save_locally(list_id,list)
            print("Changes saved")
            print("Do you want to send the changes to the server? (y/n)")
            
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

