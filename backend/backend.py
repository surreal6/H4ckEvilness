from flask import Flask, make_response, render_template, request
from functions import generate_email_hash

app = Flask(__name__)


@app.route('/emailDeprecated/<emailInput>/')
def email(emailInput):
    print(generate_email_hash(emailInput))
    return 'Correaco! '+emailInput


@app.route('/email/')
def email2():
    # TODO. Check db
    # TODO. Return url with 201 and url @Location.
    email_in = request.args.get('email')
    hash = generate_email_hash(email_in)
    resp = make_response('202', 202)
    resp.headers['Location'] = '/url/'+hash+"/"
    return resp

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
