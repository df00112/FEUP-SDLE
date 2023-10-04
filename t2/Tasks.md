# Tasks for the 2nd class:

1. ~~Study the zmq_poll() function.~~
1. ~~Adapt the publisher in the 1st class to broadcast weather updates for PT zipcodes (4 digits). Adapt the client subscriber, using the poll mechanism, to fetch data from two publishers, one US and the other PT.~~
1. Implement and test the shared queue pattern (with dealer and router sockets).
    1. Try running a single client and worker, with the broker.
    2. Try adding another worker and see the distribution of requests.
    3. Try killing and re-starting the broker.
    4. Try to emulate network partitions (e.g. by running the different processes in different laptops and switching off the appropriate network
interfaces).
1. Implement and test a proxy to allow a client to subscribe to topics that are published by an unknown number of subscribers (dynamic discovery
problem) using the XSUB and the XPUB sockets.
    1. ~~Try to implement the proxy by adapting the broker of the shared queue pattern.~~
    2. ~~Adapt the publisher from the broadcast weather updates example.~~
    3. ~~Adapt the subscriber from the broadcast weather updates example~~
    4. Try killing and re-starting the proxy.
    5. Try to emulate network partitions (e.g. by running the different processes in different laptops and switching off the appropriate network interfaces).
