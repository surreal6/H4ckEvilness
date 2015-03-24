import time
import zmq
from zmq.backend.cython.socket import ZMQError

PUB_PORT = "5500"


class SocketPublisher:

    context = None
    socket = None

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        try:
            self.socket.bind("tcp://*:%s" % PUB_PORT)
        except ZMQError:
            print "Bind failed"
            self.socket.close()
            self.socket = self.context.socket(zmq.PUB)

    def __del__(self):
        # print "__del__"
        self.socket.close()

    def send_string(self, unicode_str):
        print " [*] Sending string to socket"
        # TODO. Technical debt
        time.sleep(0.5)
        self.socket.send_string(unicode_str)

    def close(self):
        self.socket.close()
        self.context.term()