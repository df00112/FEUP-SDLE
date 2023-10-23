import json
if __name__ == '__main__':
    # Create a dictionary to store data for multiple individuals
    data = {
        "john_doe": {
            "name": "John Doe",
            "age": 30,
            "items": {
                "apples": {
                    "quantity": 10,
                    "bought": False
                }
            }
        },
        "phill_doe": {
            "name": "Phill Doe",
            "age": 35,
            "items": {
                "apples": {
                    "quantity": 15,
                    "bought": True
                }
            }
        }
    }

    # Add a "bananas" item for "John Doe"
    data["john_doe"]["items"]["bananas"] = {
        "quantity": 5,
        "bought": True  # For example, John Doe has bought bananas
    }

    # save the data to a json file
    # Serialize the dictionary to a JSON string
    json_data = json.dumps(data)
    with open("./data/cloud/list_data.json", "w") as f:
        json.dump(json_data, f, indent=4)

    user_data = {
        "john_doe": {
            "name": "John Doe",
            "password": "123456"
        }
    }

    json_data = json.dumps(user_data)
    with open("./data/cloud/user_data.json", "w") as f:
        json.dump(json_data, f, indent=4)

    local_data = data
    