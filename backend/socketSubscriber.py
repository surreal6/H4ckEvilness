import zmq
from functions import generate_email_hash
from servicesWorker.mainWorker import ServiceWorker

port = "5500"

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print "Collecting emails..."
socket.connect("tcp://localhost:%s" % port)
socket.setsockopt(zmq.SUBSCRIBE, "email")

while True:
    string = socket.recv()
    key, value = string.split('|')
    ServiceWorker("email", generate_email_hash(value)).start()
    print "email>"+value
