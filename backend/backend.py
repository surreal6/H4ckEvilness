from flask import Flask
from functions import generate_email_hash

app = Flask(__name__)


@app.route('/email/<emailInput>/')
def email(emailInput):
    # TODO. Check db
    print(generate_email_hash(emailInput))
    # TODO. Return url with 301 and url @Location.
    return 'Correaco! '+emailInput


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
