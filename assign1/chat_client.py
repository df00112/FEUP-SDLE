import zmq
import threading

username = ""
subcribed_topics = []
sub_socket = None
pub_socket = None


# init handles the initialization of the chat client, asks for username
def init():
    print("Welcome to the chat client!")
    username = input("Please enter your username: ")
    print("Welcome, " + username + "!")

# Main cycle of the chat client
def main():

# Asks for input (topic) from the user to subscribe to a topic
def subscribe_topic():

# Asks for input (topic) from the user to unsubscribe from a topic
def unsubscribe_topic():

# Asks for which topic the user wants to publish to, then asks for the message
def pub_side():

# Receives messages from the server and prints them out
def sub_side():

if __name__ == "__main__":
    init()