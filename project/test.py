import json
if __name__ == '__main__':
    # Create a dictionary to store data for multiple individuals
    data = {
        "john_doe": {
            "name": "John Doe",
            "password": "123456",
            "lists": {
                "5556": {
                    "id": "5556",
                    "name":"Compras para amanhã",
                    "owner": "john_doe",
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
                    "id": "5557",
                    "name": "Compras para hoje",
                    "owner": "john_doe",
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
                    "id": "5557",
                    "name": "Compras para hoje",
                    "owner": "jhon_doe",
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
    
    data = {
        "5556": {
            "id": "5556",
            "name":"Compras para amanhã",
            "owner": "john_doe",
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
            "id": "5557",
            "name": "Compras para hoje",
            "owner": "john_doe",
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

    json_data = json.dumps(data)
    with open("./data/cloud/data.json", "w") as f:
        json.dump(json_data, f, indent=4)

    cloud_data = data

    print(cloud_data.keys())

    # nem todos os servers precisam de ter todos as listas, uns servers tratam de x listas
