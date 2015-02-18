import hashlib
import time
from flask import make_response
import zmq
from zmq.backend.cython.socket import ZMQError
from requestDb import RequestDB

KEY = "MK7Bl7O903"
PUB_PORT = "5557"

context = zmq.Context()
socket = context.socket(zmq.PUB)
time.sleep(1)
try:
    socket.bind("tcp://*:%s" % PUB_PORT)
except ZMQError:
    socket.close()
    socket = context.socket(zmq.PUB)
    # socket.bind("tcp://*:%s" % PUB_PORT)


def generate_email_hash(email_in):
    return hashlib.sha224(email_in+KEY).hexdigest()


def publish_to_queue_email(email_in):
    socket.send_string("email|%s" % email_in)


def get_uncompleted_request(urlIn):
    resp = make_response('301', 202)
    resp.headers['Location'] = '/url/'+urlIn+"/"
    resp.headers['location'] = '/url/'+urlIn+"/"
    resp.headers['Retry-After]'] = '2'
    return resp


def get_model(key, hash):
    # TODO. Connect to GraphDB.
    db = RequestDB()
    return make_response(str(db.query("SELECT * FROM Request WHERE Hash='"+str(hash)+"'")), 200)
