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
    with open("./data/cloud/serialized_data.json", "r") as f:
        json_data = json.load(f)


    data = json_data
    sets=[]
    for lst in data:
        aux=json.loads(lst)
        aworset=json_to_aworset(aux)
        sets.append(aworset)
    
    print("SETS")
    for aworset in sets:
        aworset.all_info()
    
    
    ooo=sets[0]

    
    ooo.all_info()
    update_list(ooo)
    
    """ json_data.append(json_data[0])
    
    with open("./data/cloud/seridata.json", "w") as json_file:
        json.dump(json_data, json_file, indent=2) """
    
    
    
awoga()
