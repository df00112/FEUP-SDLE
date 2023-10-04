#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq


def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        #  Wait for next request from client
        try:
            message = socket.recv()
            print(f"Received request: {message}")
        except zmq.error.Again:
            print("Timeout")
            break

        #  Do some 'work'
        time.sleep(1)

        #  If request is "exit" then kill the server
        if message == b"kill":
            print("Server is shutting down...")
            break

        #  Send reply back to client
        socket.send_string("World")


def main():
    while True:
        print("Starting server...")
        server()

if __name__ == "__main__":
    main()
