import zmq
import random
import sys
import time

context = zmq.Context()
PORT = "5557"

if len(sys.argv) > 2:
    key = sys.argv[1]
    value = sys.argv[2]

socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % PORT)

while True:
    topic = random.randrange(9999,10005)
    messagedata = random.randrange(1,215) - 80
    print "%d %d" % (topic, messagedata)
    socket.send("%d %d" % (topic, messagedata))
    time.sleep(1)