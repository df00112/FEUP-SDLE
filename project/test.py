import json
if __name__ == '__main__':
    # Create a dictionary to store data for multiple individuals
    data = {
        "john_doe": {
            "name": "John Doe",
            "password": "123456",
            "lists": {
                "5556": {
                    "name":"Compras para amanhã",
                    "lastUpdate": "2021-03-01 12:00:00",
                    "apples": {
                        "quantity": 10,
                        "bought": False
                    },
                    "bananas": {
                        "quantity": 5,
                        "bought": True
                    },
                    "oranges": {
                        "quantity": 3,
                        "bought": False
                    }
                },
                "5557": {
                    "name": "Compras para hoje",
                    "lastUpdate": "2021-05-01 12:00:00",
                    "water": {
                        "quantity": 15,
                        "bought": True
                    },
                    "chicken": {
                        "quantity": 2,
                        "bought": True
                    },
                }
            }
        },
        "phill_doe": {
            "name": "Phill Doe",
            "password": "123456",
            "lists": {
                "5557": {
                    "name": "Compras para hoje",
                    "lastUpdate": "2021-05-01 12:00:00",
                    "water": {
                        "quantity": 15,
                        "bought": True
                    },
                    "chicken": {
                        "quantity": 2,
                        "bought": True
                    },
                }
            }
        }
    }

    # save the data to a json file
    # Serialize the dictionary to a JSON string
    json_data = json.dumps(data)
    with open("./data/local/users.json", "w") as f:
        json.dump(json_data, f, indent=4)

    local_data = data
    