from flask import Flask, make_response, request
from functions import generate_email_hash, publish_to_queue_email, get_uncompleted_request, get_model
from requestDb import RequestDB

app = Flask(__name__)


@app.route('/email/', methods=[u'GET'])
def email():
    email_in = request.args.get('email')
    hash = generate_email_hash(email_in)
    resp = make_response('202', 301)
    resp.headers['Location'] = '/url/'+hash+"/"
    resp.headers['Retry-After]'] = '5'
    publish_to_queue_email(email_in)
    db = RequestDB()
    db.set_request("email", hash)
    return resp


@app.route('/url/<hash>/')
def url(hash):
    db = RequestDB()
    if db.get_request_code("email", hash) is 202:
        print "Not in db"
        db.set_request_finished("email", hash)
        return get_uncompleted_request(hash)
    else:
        model = get_model("email", hash)
        db.remove_request("email", hash)
        return model


if __name__ == '__main__':
    app.run(debug=True)
