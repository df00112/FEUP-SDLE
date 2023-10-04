# Espresso Pattern
# This shows how to capture data using a pub-sub proxy
#

import time

from random import randint
from threading import Thread

import zmq

# The subscriber thread requests messages starting with
# A and B, then reads and counts incoming messages.

def subscriber_thread():
    ctx = zmq.Context.instance()

    # Subscribe to "A" and "B"
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:6001")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"A")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"B")
    #subscriber.setsockopt(zmq.SUBSCRIBE, b"")

    count = 0
    while True:
        try:
            msg = subscriber.recv_multipart()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted
            else:
                raise
        count += 1

    print ("Subscriber received %d messages" % count)


# .split publisher thread
# The publisher sends random messages starting with A-J:

def publisher_thread():
    ctx = zmq.Context.instance()

    publisher = ctx.socket(zmq.PUB)
    publisher.connect("tcp://localhost:6000")
    count = 0
    while True:
        string = "AAAA"
        try:
            count += 1
            publisher.send(string)
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted
            else:
                raise
        time.sleep(0.1)         # Wait for 1/10th second
    print ("publisher sent out {0} messages".format(count))


# .split listener thread
# The listener receives all messages flowing through the proxy, on its
# pipe. Here, the pipe is a pair of ZMQ_PAIR sockets that connects
# attached child threads via inproc. In other languages your mileage may vary:

def listener_thread (pipe):

    # Print everything that arrives on pipe
    count = 0
    while True:
        try:
            count += 1
            pipe.recv_multipart()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted
    print ("listener saw {0} messages".format(count))

# .split main thread
# The main task starts the subscriber and publisher, and then sets
# itself up as a listening proxy. The listener runs as a child thread:

def main ():

    # Start child threads
    ctx = zmq.Context.instance()
    p_thread = Thread(target=publisher_thread)
    s_thread = Thread(target=subscriber_thread)

    pipe = zpipe(ctx)

    subscriber = ctx.socket(zmq.XSUB)
    subscriber.bind("tcp://*:6000")

    publisher = ctx.socket(zmq.XPUB)
    publisher.bind("tcp://*:6001")

    l_thread = Thread(target=listener_thread, args=(pipe[1],))
    print ('going to sleep')
    time.sleep(1)
    print ('awake starting threads')
    l_thread.start()
    p_thread.start()
    s_thread.start()
    try:
        monitored_queue(subscriber, publisher, pipe[0], 'pub', 'sub')
    except KeyboardInterrupt:
        print ("Interrupted")

    del subscriber, publisher, pipe
    ctx.term()

if __name__ == '__main__':
    main()