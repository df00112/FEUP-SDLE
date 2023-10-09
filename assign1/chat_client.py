import zmq
import threading

def receive_messages():
    while True:
        message = subscriber.recv_string()
        
        message=message.split(" ")
        topic = message[0]
        username = message[1]
        content = ' '.join(message[2:])
        with open("chat_log.txt", "a") as log_file:
            log_file.write("User: "+username+" Topic: "+topic+" Message: "+content+"\n")
        #print(f"Received: {message}")

context = zmq.Context()

# Create a PUB socket for broadcasting messages
publisher = context.socket(zmq.PUB)
publisher.connect("tcp://localhost:5560")

# Create a SUB socket for receivingx messages from other clients
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5559")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

# Start a thread to receive messages in the background
receiver_thread = threading.Thread(target=receive_messages)
receiver_thread.daemon = True
receiver_thread.start()

try:
    while True:
        message = input("Topic Username Message:")
        if(message==""):
            continue
        message=message.split(" ")
        topic = message[0]
        username = message[1]
        content = ' '.join(message[2:])
        publisher.send_string(f'{topic} {username} {content}')
except KeyboardInterrupt:
    pass
finally:
    publisher.close()
    subscriber.close()
    context.term()


 