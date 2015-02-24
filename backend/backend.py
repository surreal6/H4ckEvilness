from flask import Flask, make_response, request
from databases.mainDb import MainDB

from functions import publish_to_queue_email, get_uncompleted_request, get_model, get_unfound_url
from databases.requestDb import RequestDB


app = Flask(__name__)


@app.route('/email/', methods=[u'GET'])
def email():
    email_in = str(request.args.get('email'))
    publish_to_queue_email(email_in)
    db = RequestDB()
    db.set_request("email", email_in)
    maindb = MainDB()
    if not maindb.is_user_in_db(email=email_in):
        user_id = maindb.put_user_by_email(email_in)
    else:
        user = maindb.get_user_by_email(email_in)
        user_id = user['id']
        user_status = user['status']
        if user_status is 200:
            maindb.set_user_updating(user_id=user_id)
    resp = make_response('202', 301)
    location_url = '/url/'+str(user_id)+"/"
    print location_url
    resp.headers['Location'] = location_url
    resp.headers['Retry-After]'] = '5'

    return resp


@app.route('/url/<user_id>/')
def url(user_id):
    maindb = MainDB()
    user = maindb.get_user(user_id=user_id)
    if not user:
        return get_unfound_url()
    elif user['status'] is not 200:
        # maindb.set_user_status(user_id=user['id'], status=200)
        return get_uncompleted_request(user_id)
    else:
        return str(user)


if __name__ == '__main__':
    app.run(debug=True)
