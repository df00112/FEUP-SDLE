# Client (REQ)
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

socket.send(b"Hello")
reply = socket.recv_multipart()
print(reply)
