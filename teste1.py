# Server (ROUTER)
import zmq

context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv_multipart()
    print(f"Received request from identity : {message}")
    # Process the request and send a reply back to the same identity
    socket.send_multipart([ b'pong'])
