import hashlib
import string

from flask import make_response
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from unidecode import unidecode
from Sockets.publisher import SocketPublisher


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


def get_tag_value(node):
    """retrieves value of given XML node
    parameter:
    node - node object containing the tag element produced by minidom

    return:
    content of the tag element as string
    """

    xml_str = node  # flattens the element to string

    # cut off the base tag to get clean content:
    start = xml_str.find('>')
    if start == -1:
        return ''
    end = xml_str.rfind('<')
    if end < start:
        return ''

    return xml_str[start + 1:end]


def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])
