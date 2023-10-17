import zmq
import time

context = zmq.Context()

#  Socket to talk to the server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

total_time = 0  # Initialize total time

# Set a timeout (in milliseconds)
timeout = 5000  # 5 seconds

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

# Loop and accept messages from both channels, acting accordingly
while True:
    socket.send_string("Hello")
    print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    socks = dict(poller.poll(2000))
    print("YOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    if socks:
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa")
        if socks.get(socket) == zmq.POLLIN:
            print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
            message = socket.recv_string(zmq.NOBLOCK)
            print ("got message "+ message)
    else:
        print ("error: message timeout")
