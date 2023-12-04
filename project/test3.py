from utils import *
import json
from AWORSet import AWORSet



def haha():

    with open("./data/cloud/data.json", "r") as f:
        json_data = json.load(f)


    data = json.loads(json_data)

    lists=[]

    for key in data:
        aworset=AWORSet(data[key]["id"],data[key]["name"],data[key]["owner"])
        for item in data[key]["items"]:
            aworset.add_new(item,data[key]["items"][item]["quantity"],data[key]["items"][item]["bought"])
        
        lists.append(aworset) 
        
    json_list=[]
    for aworset in lists:
        serialized_data=aworset_to_json(aworset)
        json_list.append(serialized_data)
        

    # Now you can do something with the json_list, such as writing it to a new JSON file
    with open("./data/cloud/serialized_data.json", "w") as json_file:
        json.dump(json_list, json_file, indent=2)


def awoga():
    with open("./data/cloud/data.json", "r") as f:
        json_data = json.load(f)


    data = json_data
    sets=[]
    for lst in data:
        aux=json.loads(lst)
        aworset=json_to_aworset(aux)
        sets.append(aworset)
    
    print("SETS")
    for aworset in sets:
        #aworset.all_info()
        i=1
    
    
    ooo=sets[0]
    ooo.lookup()
    
    
    #ooo.all_info()
    #update_list(ooo)
    
    """ json_data.append(json_data[0])
    
    with open("./data/cloud/seridata.json", "w") as json_file:
        json.dump(json_data, json_file, indent=2) """
    
    
    
def read_user_info():
    with open("./data/local/users.json", "r") as f:
        data = json.load(f)
        

    data = json.loads(data)

    first_key=list(data.keys())[0]
    for lst in data[first_key]["lists"]:
        print("Lst:",lst)
    
     # display the shopping lists
    print("\n=====================================")
    username="john_doe"
    list_keys = list(data[username]["lists"].keys())
    print(f"Shopping lists: {list_keys}")
    print("Shopping lists:")

    for username in data:   
        for list_id in data[username]["lists"]:
            ia=list_id
            print(f"{list_id}: {data[username]['lists'][list_id]['list_name']} ")
            aworset=json_to_aworset(data[username]['lists'][list_id])
            json_data=aworset_to_json(aworset)
            data[username]["lists"][list_id]=json_data

    json_data = json.dumps(data)
    with open("./data/local/users4.json", "w") as f:
        json.dump(json_data, f, indent=2)



def read_data():
    with open("./data/local/users4.json", "r") as f:
        json_data = json.load(f)
        
        data=json.loads(json_data)
        
        for username in data:
            print("Username:",username)
            for list_id in data[username]["lists"]:
                print("list_id:",list_id)
                lst=json.loads(data[username]["lists"][list_id])
                aworset=json_to_aworset(lst)
                aworset.all_info()
                break
            break
    """ lists=[]

    for key in data:
        aworset=AWORSet(data[key]["id"],data[key]["name"],data[key]["owner"])
        for item in data[key]["items"]:
            aworset.add_new(item,data[key]["items"][item]["quantity"],data[key]["items"][item]["bought"])
        
        lists.append(aworset) 
    
    for aworset in lists:
        aworset.all_info() """
    
    
    


if __name__ == "__main__":
    read_data()

