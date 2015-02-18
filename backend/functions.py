import hashlib
import time
import zmq

KEY = "MK7Bl7O903"
PUB_PORT = "5557"

context = zmq.Context()
socket = context.socket(zmq.PUB)
time.sleep(1)


def generate_email_hash(email_in):
    return hashlib.sha224(email_in+KEY).hexdigest()


def publish_to_queue_email(email_in):
    socket.bind("tcp://*:%s" % PUB_PORT)
    # TODO. Remove this SHIT.
    time.sleep(0.2)
    socket.send_string("email|%s" % email_in)
    socket.unbind("tcp://*:%s" % PUB_PORT)