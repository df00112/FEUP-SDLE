from AWORSet import AWORSet
import json
import uuid

def generate_unique_url(attribute_value):
    unique_id = uuid.uuid4()
    # Replace any non-alphanumeric characters with dashes
    clean_attribute_value = ''.join(c if c.isalnum() else '-' for c in str(attribute_value))
    url = f'/attribute/{clean_attribute_value}/{unique_id}'
    return url

# Example usage
attribute_value = "example attribute"
unique_url = generate_unique_url(attribute_value)
print(unique_url)

with open("./data/cloud/data.json", "r") as f:
        data = json.load(f)



data = json.loads(data)

lists=[]

for key in data:
    aworset=AWORSet(data[key]["id"],data[key]["name"],data[key]["owner"])
    for item in data[key]["items"]:
        aworset.add(item,data[key]["items"][item]["quantity"],data[key]["items"][item]["bought"])
    
    lists.append(aworset)
    
