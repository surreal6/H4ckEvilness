import time
import zmq

port = "5557"

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print "Collecting emails..."
socket.connect("tcp://localhost:%s" % port)
socket.setsockopt(zmq.SUBSCRIBE, "email")

while True:
    string = socket.recv()
    key, value = string.split('|')
    # TODO. Send to worker.
    print "email>"+value
