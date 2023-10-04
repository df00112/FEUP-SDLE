import zmq
from random import randrange
def server():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://localhost:5560")

    print ("Starting server...")
    while True:
        print ("Sending message...")
        zipcode = randrange(1, 100000)
        temperature = randrange(-80, 135)
        relhumidity = randrange(10, 60)
        temp=str(zipcode)+" "+str(temperature)+" "+str(relhumidity) + " US"
        socket.send_string(temp)
        print ("Message sent!")

if __name__ == "__main__":
    server()