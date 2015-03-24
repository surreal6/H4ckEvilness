import zmq
from servicesWorker.mainWorker import MainWorker

port = "5500"

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print "Collecting emails..."
socket.connect("tcp://localhost:%s" % port)
socket.setsockopt(zmq.SUBSCRIBE, "email")

while True:
    string = socket.recv()
    key, value, user_id = string.split('|')
    MainWorker("email", value, user_id).start()
