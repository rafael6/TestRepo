import sys

import requests

print(sys.version)
print(sys.executable)
print('hello world')



name = input('what is your name?')
print(name)

r = requests.get('https://cnn.com')
print(r.status_code)
