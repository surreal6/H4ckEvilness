# H4ckEvilness

El maligno


# Install

Tested in Ubuntu 14.04 and 15.04.

    sudo apt-get install libpq-dev python-dev libxslt1-dev libxslt1.1 libxml2-dev libxml2 libssl-dev postgresql python-psycopg2 rabbitmq-server  

    git clone git@github.com:H4ckEvilness/H4ckEvilness.git
    cd H4ckEvilness
    sudo sh prior.sh


# Config

The database needs to be set up before running the server:

    sudo -u postgres createuser -P maligno
    sudo -u postgres createdb evilDatabase -O maligno

Use `ePvP4quXsHvp` as user password.


# Run

There are three processes that need to be run simultaneously:

    python backend/backend.py
    python backend/servicesRaiser.py
    python backend/socketSubscriber.py

The server is at http://127.0.0.1:5000/. Go to http://127.0.0.1:5000/email/?email=mariano.rajoy@pp.es to make a request.