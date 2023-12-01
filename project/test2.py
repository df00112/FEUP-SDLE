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
#print(unique_url)

with open("./data/cloud/data.json", "r") as f:
        data = json.load(f)



data = json.loads(data)

lists=[]

for key in data:
    aworset=AWORSet(data[key]["id"],data[key]["name"],data[key]["owner"])
    for item in data[key]["items"]:
        aworset.add(item,data[key]["items"][item]["quantity"],data[key]["items"][item]["bought"])
    
    lists.append(aworset)

# Assuming lists[0] is an instance of AWORSet

""" awor_set_instance = lists[0]

# Convert tuple keys to strings in all relevant attributes

converted_items = {str(key): value for key, value in awor_set_instance.items.items()}

# Serialize the object with the modified attributes
serialized_data = json.dumps({
    "list_id": awor_set_instance.list_id,
    "list_name": awor_set_instance.list_name,
    "owner": awor_set_instance.owner,
    "cCounter": awor_set_instance.cCounter,
    "context": list(awor_set_instance.context),
    "items": converted_items
}, default=lambda x: x.__dict__)

# Print or send the serialized_data as needed
print(serialized_data)
json_data = json.dumps(serialized_data)
with open("./data/teste.json", "w") as f:
    json.dump(serialized_data, f, indent=4)  
     """

""" json_string = "{\"list_id\": \"aea1e6f6-ef2c-4bff-b131-78277eef05d3\", \"list_name\": \"Compras para amanh\\u00e3\", \"owner\": \"john_doe\", \"cCounter\": 4, \"context\": [[\"bananas\", 2], [\"oranges\", 3], [\"apples\", 1]], \"items\": {\"('apples', 1)\": {\"name\": \"apples\", \"quantity\": {\"positive_counter\": {\"gn_counter\": 10}, \"negative_counter\": {\"gn_counter\": 0}}, \"bought_status\": {\"positive_counter\": {\"gn_counter\": false}, \"negative_counter\": {\"gn_counter\": 0}}}, \"('bananas', 2)\": {\"name\": \"bananas\", \"quantity\": {\"positive_counter\": {\"gn_counter\": 5}, \"negative_counter\": {\"gn_counter\": 0}}, \"bought_status\": {\"positive_counter\": {\"gn_counter\": true}, \"negative_counter\": {\"gn_counter\": 0}}}, \"('oranges', 3)\": {\"name\": \"oranges\", \"quantity\": {\"positive_counter\": {\"gn_counter\": 3}, \"negative_counter\": {\"gn_counter\": 0}}, \"bought_status\": {\"positive_counter\": {\"gn_counter\": false}, \"negative_counter\": {\"gn_counter\": 0}}}}}"
try:
    # Parse the JSON string
    data = json.loads(json_string)

    # Print the parsed data for debugging
    print("Parsed JSON data:")
    print(data)

    # Access specific values
    print("\nList ID:", data["list_id"])
    print("List Name:", data["list_name"])
    print("Owner:", data["owner"])
    print("Counter:", data["cCounter"])

    # Access context and items
    print("\nContext:")
    for context_item in data["context"]:
        print(context_item)

    print("\nItems:")
    for item_key, item_data in data["items"].items():
        print("Item Key:", item_key)
        print("Item Name:", item_data["name"])
        print("Quantity:", item_data["quantity"]["positive_counter"]["gn_counter"])
        print("Bought:", item_data["items"][item_key]["bought_status"]["positive_counter"]["gn_counter"])

except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

exit() """
with open("./data/teste.json", "r") as f:
        json_data = json.load(f)

#print(json_data)


data = json.loads(json_data)

print(data)

print("\nList ID:", data["list_id"])
print("List Name:", data["list_name"])
print("Owner:", data["owner"])
print("Counter:", data["cCounter"])

# Access context and items
print("\nContext:")
for context_item in data["context"]:
    print(context_item)

print("\nItems:")
for item_key, item_data in data["items"].items():
    print("Item Key:", item_key)
    print("Item Name:", item_data["name"])
    print("Quantity:", item_data["quantity"]["positive_counter"]["gn_counter"]-item_data["quantity"]["negative_counter"]["gn_counter"])
    print("Bought:", item_data["bought_status"]["positive_counter"]["gn_counter"]-item_data["bought_status"]["negative_counter"]["gn_counter"])


exit()
for item_id, item_data in data.items():
    print(f"Item ID: {item_id}")
    print(f"Item Name: {item_data['name']}")
    print(f"Owner: {item_data['owner']}")
    print(f"Last Update: {item_data['lastUpdate']}")
    
    # Iterate over the nested items
    print("Items:")
    for item_name, item_details in item_data['items'].items():
        print(f"  - {item_name}: Quantity {item_details['quantity']}, Bought: {item_details['bought']}")

    print("\n") 