
import os
from PIL import Image
from IPython.display import IFrame
import requests
import tempfile

# Fetching a text webpage 
url = 'https://www.ibm.com/'
r = requests.get(url)   
print(r.status_code)
print(r.request.headers)                        # headers sent in the request  
print(f'Date fetched = {r.headers['date']}')    # r.headers are response headers


# fetch an image 
url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0101EN-SkillsNetwork/IDSNlogo.png'
r = requests.get(url)
print(f'Content type is {r.headers['content-type']}')  # content type of the response
# store the file in a temporary file
with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
    fp.write(r.content)
    fp.close()

    img = Image.open(fp.name)
    img.show()

# Show how we construct a URL with parameters
print("\n\nExample of constructing a URL with parameters")

url_get = 'http://httpbin.org/get'
payload = {"name":"Joseph", "ID":"123"}
r = requests.get(url_get, params=payload) 
# See the request details 
print(r.url)             # http://httpbin.org/get?name=Joseph&ID=123
print(r.request.body)    # none. Nothing in the body
print(r.status_code, r.request.headers)

