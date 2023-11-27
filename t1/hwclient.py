import zmq
import time

context = zmq.Context()

# Socket to talk to the server
print("Connecting to REQ-ROUTER server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Set a timeout (in milliseconds)
timeout = 5000  # 5 seconds

# Loop to send multiple requests
for _ in range(5):
    socket.send_string("Hello")

    # Create a poller and register the socket for POLLIN event
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    # Wait for the specified timeout for a response
    socks = dict(poller.poll(timeout))
    if socket in socks and socks[socket] == zmq.POLLIN:
        # Receive reply from server
        message = socket.recv_string()
        print(f"Received reply: {message}")
    else:
        print("Timeout: No response from the server within the specified time")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
    #time.sleep(1)  # Wait between requests

socket.close()
context.term()
