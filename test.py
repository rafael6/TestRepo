import sys

import requests

print(sys.version)
print(sys.executable)
print('Hello World')

r = requests.get('https://cnn.com')
print(r.status_code)
