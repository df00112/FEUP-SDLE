from kademlia.network import Server
import asyncio

async def main():
    # Create a Kademlia node
    server = Server()
    
    # Start the node and listen on a specific address and port
    server.listen(8468)

    # Bootstrap from an existing node (replace with actual node address and port)
    #server.bootstrap([("123.123.123.123", 5678)])

    # Store a key-value pair in the DHT
    await server.set("my_key", "my_value")

    # Retrieve a value from the DHT
    result = await server.get("my_key")
    print("Retrieved value:", result)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
