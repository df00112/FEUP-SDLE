import json
import uuid
if __name__ == '__main__':
    # Create a dictionary to store data for multiple individuals
    list_id=[]
    list_id.append(str(uuid.uuid4()))
    list_id.append(str(uuid.uuid4()))
    data = {
    "john_doe": {
      "name": "John Doe",
      "password": "123456",
      "lists": {
        "aea1e6f6-ef2c-4bff-b131-78277eef05d3": {
            "list_id": "aea1e6f6-ef2c-4bff-b131-78277eef05d3",
            "list_name": "Compras para amanhã",
            "owner": "john_doe",
            "cCounter": 4,
            "context": [
              ["oranges", 3],
              ["apples", 1],
              ["bananas", 2]
            ],
            "items": {
              "('apples', 1)": {
                "name": "apples",
                "quantity": {
                  "positive_counter": {"gn_counter": 10},
                  "negative_counter": {"gn_counter": 0}
                },
                "bought_status": {
                  "positive_counter": {"gn_counter": 0},
                  "negative_counter": {"gn_counter": 0}
                }
              },
              "('bananas', 2)": {
                "name": "bananas",
                "quantity": {
                  "positive_counter": {"gn_counter": 5},
                  "negative_counter": {"gn_counter": 0}
                },
                "bought_status": {
                  "positive_counter": {"gn_counter": 1},
                  "negative_counter": {"gn_counter": 0}
                }
              },
              "('oranges', 3)": {
                "name": "oranges",
                "quantity": {
                  "positive_counter": {"gn_counter": 3},
                  "negative_counter": {"gn_counter": 0}
                },
                "bought_status": {
                  "positive_counter": {"gn_counter": 0},
                  "negative_counter": {"gn_counter": 0}
                }
              }
            }
          },
        "03bf3c0d-b691-4cb6-8860-a3d2ab38eed5":{
            "list_id": "03bf3c0d-b691-4cb6-8860-a3d2ab38eed5",
            "list_name": "Compras para hoje",
            "owner": "john_doe",
            "cCounter": 3,
            "context": [
              ["water", 1],
              ["chicken", 2]
            ],
            "items": {
              "('water', 1)": {
                "name": "water",
                "quantity": {
                  "positive_counter": {"gn_counter": 15},
                  "negative_counter": {"gn_counter": 0}
                },
                "bought_status": {
                  "positive_counter": {"gn_counter": 1},
                  "negative_counter": {"gn_counter": 0}
                }
              },
              "('chicken', 2)": {
                "name": "chicken",
                "quantity": {
                  "positive_counter": {"gn_counter": 2},
                  "negative_counter": {"gn_counter": 0}
                },
                "bought_status": {
                  "positive_counter": {"gn_counter": 1},
                  "negative_counter": {"gn_counter": 0}
                }
              }
            }
          }
          
      }
    },
    "phill_doe": {
      "name": "Phill Doe",
      "password": "123456",
      "lists": {
        "03bf3c0d-b691-4cb6-8860-a3d2ab38eed5":{
            "list_id": "03bf3c0d-b691-4cb6-8860-a3d2ab38eed5",
            "list_name": "Compras para hoje",
            "owner": "john_doe",
            "cCounter": 3,
            "context": [
              ["water", 1],
              ["chicken", 2]
            ],
            "items": {
              "('water', 1)": {
                "name": "water",
                "quantity": {
                  "positive_counter": {"gn_counter": 15},
                  "negative_counter": {"gn_counter": 0}
                },
                "bought_status": {
                  "positive_counter": {"gn_counter": 1},
                  "negative_counter": {"gn_counter": 0}
                }
              },
              "('chicken', 2)": {
                "name": "chicken",
                "quantity": {
                  "positive_counter": {"gn_counter": 2},
                  "negative_counter": {"gn_counter": 0}
                },
                "bought_status": {
                  "positive_counter": {"gn_counter": 1},
                  "negative_counter": {"gn_counter": 0}
                }
              }
            }
          }
      }
    }
  }

    # save the data to a json file
    # Serialize the dictionary to a JSON string
    json_data = json.dumps(data)
    with open("./data/local/users.json", "w") as f:
        json.dump(json_data, f, indent=10) 

    local_data = data
    
    data = {
        list_id[0]: {
            "list_id": list_id[0],
            "list_name":"Compras para amanhã",
            "owner": "john_doe",
            "items":{
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
            }
        },
        list_id[1]: {
            "id": list_id[1],
            "name": "Compras para hoje",
            "owner": "john_doe",
            "lastUpdate": "2021-05-01 12:00:00",
            "items":{
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

    json_data = json.dumps(data)
    """ with open("./data/cloud/data.json", "w") as f:
        json.dump(json_data, f, indent=4) """

    cloud_data = data

    print(cloud_data.keys())

    # nem todos os servers precisam de ter todos as listas, uns servers tratam de x listas
