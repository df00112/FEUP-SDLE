import time
import zmq

def server():
    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind("tcp://*:5555")

    while True:
        #  Wait for next request from client
        try:
            # Receive identity frame
            identity = socket.recv()

            # Receive empty delimiter frame
            empty = socket.recv()

            # Receive message content from client
            message = socket.recv_string()
            print(f"Received request from {identity}: {message}")

            # Do some 'work'
            time.sleep(1)

            # Send reply back to client
            print("Sending reply")
            socket.send(identity, zmq.SNDMORE)
            socket.send(b"", zmq.SNDMORE)
            socket.send_string("World")
        except zmq.error.Again:
            print("Timeout")
            break

def main():
    while True:
        print("Starting server...")
        server()

if __name__ == "__main__":
    main()
