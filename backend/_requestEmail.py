import requests
import time
import sys

if len(sys.argv) is 2:
    email = sys.argv[1]
else:
    email = "mariano.rajoy@pp.es"

print email
r = requests.get('http://127.0.0.1:5000/email/?email='+email)

url = r.headers['Location']
print "Redirect to: "+url

for i in range(15):
    r = requests.get(url)
    if r.status_code is 200:
        print r.text
        break
    else:
        print "Not yet"
        time.sleep(1)
