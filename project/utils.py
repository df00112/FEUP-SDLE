from AWORSet import AWORSet
import json

def json_to_aworset(data):
   
    print(data['list_id'])
    
    
    aworset=AWORSet(data['list_id'],data['list_name'],data['owner'],data["cCounter"])
    
    for context in data['context']:
        aworset.context.add(tuple(context))
    
    
    for item_key, item_data in data["items"].items():
        quantity_positive_counter=item_data["quantity"]["positive_counter"]["gn_counter"]
        quantity_negative_counter=item_data["quantity"]["negative_counter"]["gn_counter"]
        
        bought_status_positive_counter=item_data["bought_status"]["positive_counter"]["gn_counter"]
        bought_status_negative_counter=item_data["bought_status"]["negative_counter"]["gn_counter"]
        
        tupl=eval(item_key)
        aworset.add_existing(tupl,quantity_positive_counter,bought_status_positive_counter)
        aworset.items[tupl].inc_quantity_negative_counter(quantity_negative_counter)
        aworset.items[tupl].inc_bought_status_negative_counter(bought_status_negative_counter)    
        
    return aworset


def aworset_to_json(aworset):
    converted_items = {str(key): value for key, value in aworset.items.items()}
    serialized_data = json.dumps({
        "list_id": aworset.list_id,
        "list_name": aworset.list_name,
        "owner": aworset.owner,
        "cCounter": aworset.cCounter,
        "context": list(aworset.context),
        "items": converted_items
    }, default=lambda x: x.__dict__)
    return serialized_data

# MUDAR PARA O UTILIZADOR
def update_list(aworset):
    """ with open("./data/cloud/serialized_data.json", "r") as f:
        json_data = json.load(f)
        
    index_to_update = None
    list_id=aworset.list_id
    
    
    for i, item in enumerate(json_data):
        aux=json.loads(item)
        if "list_id" in item and aux["list_id"] == list_id:
            index_to_update = i
            break
    
    if index_to_update is not None:
        # Update the data for the specific list
        json_data[index_to_update] = aworset_to_json(aworset) 
    else:
        # List not found, add the new list
        json_data.append(aworset_to_json(aworset))

    with open("./data/cloud/serialized_data.json", "w") as f:
        json.dump(json_data, f, indent=2)
 """