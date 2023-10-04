#
#   Request-reply client in Python
#   Connects REQ socket to tcp://localhost:5559
#   Sends "Hello" to server, expects "World" back
#
import zmq

#  Prepare our context and sockets
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5559")
socket.setsockopt_string(zmq.SUBSCRIBE, "10001")

print ("Collecting updates from weather server...")

# Process 5 updates
total_temp = 0
while True:
    string = socket.recv_string()
    zipcode, temperature, relhumidity, region = string.split()
    print("Msg received: ", string)
