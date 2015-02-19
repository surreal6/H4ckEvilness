import hashlib
from flask import make_response
from Sockets.publisher import SocketPublisher
from requestDb import RequestDB

KEY = "MK7Bl7O903"


def generate_email_hash(email_in):
    return hashlib.sha224(email_in+KEY).hexdigest()


def publish_to_queue_email(email_in):
    publisher = SocketPublisher()
    publisher.send_string("email|%s" % email_in)
    publisher.close()


def get_uncompleted_request(urlIn):
    resp = make_response('301', 202)
    resp.headers['Location'] = '/url/'+urlIn+"/"
    resp.headers['location'] = '/url/'+urlIn+"/"
    resp.headers['Retry-After]'] = '2'
    return resp


def get_model(key, hash):
    # TODO. Connect to GraphDB.
    db = RequestDB()
    return make_response(str(db.get_request(key, hash)), 200)
