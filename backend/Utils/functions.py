import hashlib
import string

from flask import make_response

from Sockets.publisher import SocketPublisher
from databases.requestDb import RequestDB


KEY = "MK7Bl7O903"

def publish_to_queue_email(email_in, user_id):
    publisher = SocketPublisher()
    publisher.send_string("email|%s|%s" % (email_in, user_id,))
    publisher.close()


def get_uncompleted_request(urlIn):
    resp = make_response('Not yet', 202)
    resp.headers['Location'] = '/url/'+urlIn+"/"
    resp.headers['Retry-After]'] = '2'
    return resp


def get_unfound_url():
    resp = make_response('Not found', 404)
    resp.headers['Retry-After]'] = '2'
    return resp


def get_model(key, hash):
    # TODO. Connect to GraphDB.
    db = RequestDB()
    return make_response(str(db.get_request(key, hash)), 200)

def replace_symbols(request):
    # Custom urlencoder.
    # They specifically want %27 as the quotation which is a single quote '
    # We're going to map both ' and " to %27 to make it more python-esque
    request = string.replace(request, "'", '%27')
    request = string.replace(request, '"', '%27')
    request = string.replace(request, '+', '%2b')
    request = string.replace(request, ' ', '%20')
    request = string.replace(request, ':', '%3a')
    return request