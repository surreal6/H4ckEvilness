from flask import Flask, make_response, request
from functions import generate_email_hash, publish_to_queue_email

app = Flask(__name__)


@app.route('/email/', methods=[u'GET'])
def email():
    # TODO. Check db
    # TODO. Return url with 201 and url @Location.
    email_in = request.args.get('email')
    hash = generate_email_hash(email_in)
    resp = make_response('202', 301)
    resp.headers['Location'] = '/url/'+hash+"/"
    resp.headers['Retry-After]'] = '5'
    publish_to_queue_email(email_in)
    return resp


@app.route('/url/<urlIn>/')
def url(urlIn):
    resp = make_response('301', 200)
    resp.headers['Location'] = '/url/'+urlIn+"/"
    resp.headers['Retry-After]'] = '2'
    return resp

if __name__ == '__main__':
    app.run(debug=True)
