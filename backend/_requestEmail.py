import requests
import time

r = requests.get('http://127.0.0.1:5000/email/?email=aasdf@r.com')

url = r.headers['Location']
print "Redirect to: "+url

for i in range(5):
    r = requests.get(url)
    if r.status_code is 200:
        print r.text
        break
    else:
        print "Not yet"
        time.sleep(2)