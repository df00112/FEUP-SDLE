import zmq

def chat_proxy():
    context = zmq.Context()    

    frontend = context.socket(zmq.XPUB)  
    frontend.bind("tcp://*:5559")        


    backend = context.socket(zmq.XSUB)
    backend.bind("tcp://*:5560")

    print("Starting broker...")

    zmq.proxy(frontend, backend)

    frontend.close()
    backend.close()
    context.term()


if __name__ == "__main__":
    chat_proxy()