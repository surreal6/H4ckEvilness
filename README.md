# H4ckEvilness

El maligno


# Instalacion (para ubuntu 14.04)

## dependencias:

    sudo apt-get install libpq-dev python-dev libxslt1-dev libxslt1.1 libxml2-dev libxml2 libssl-dev

    pip install scrapy 

    git clone git@github.com:H4ckEvilness/H4ckEvilness.git
    cd H4ckEvilness
    sudo sh prior.sh

# ejecucion

    python backend/backend.py

con esto se hace correr el servidor, se puede visitar en http://127.0.0.1:5000/

si se introduce esta url:

http://127.0.0.1:5000/email/?email=mariano.rajoy@pp.es

se realiza una peticion de ese mail al server, pero a partir de aqui salen algunos errores...

hasta aqui he averiguado