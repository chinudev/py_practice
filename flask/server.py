# To run this file say 
#  flask --app server.py --debug run 

# Creates a REST server for in memory store of person
# Some tests to run 
'''
  curl -i http://127.0.0.1:5000/persons/count
  curl -i http://127.0.0.1:5000/persons/ids
  curl -i http://127.0.0.1:5000/persons/125
  curl -X DELETE -i http://127.0.0.1:5000/persons/125
  curl -i http://127.0.0.1:5000/persons/125

  # store person details in file server_body.json and run the following command 
  curl --header "Content-Type: application/json" -X POST --data-binary "@server_body.json" http://127.0.0.1:5000/persons
  curl -i http://127.0.0.1:5000/persons/ids

  curl -X POST -i http://127.0.0.1:5000/personify     # error handler 
'''

import random
from flask import Flask, request, make_response

app = Flask(__name__)

data = {
    '123' : {
        "id": "123",
        "first_name": "Tanya",
        "last_name": "Slad",
        "country": "United States",
    },
    '124' : {
        "id": "124", "first_name": "Ferdy", "last_name": "Garrow", "country": "CanadaStates",
    },
    '125' : {
        "id": "125",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "country": "Mexico",
    },
}


@app.route("/persons/count")
def get_data():
    try:
        # Check if 'data' exists and has a length greater than 0
        if data and len(data) > 0:
            return {"message": f"Data of length {len(data)} found"}
        else:
            # If 'data' is empty, return a JSON response with a 500 Internal Server Error status code
            return {"message": "Data is empty"}, 500
    except NameError:
        # Handle the case where 'data' is not defined
        # Return a JSON response with a 404 Not Found status code
        return {"message": "Data not found"}, 404


@app.route("/persons/ids")
def get_ids():
    return {"ids" : str(list(data.keys()))}


# Dynamic endpoints 
@app.route('/persons/<uid>')
def find_person(uid):
    if uid not in data:
        return {"message": f"Person with ID {uid} not found"}, 404
    
    return {"person": data[uid]}


@app.route('/persons/<uid>', methods=['DELETE'])
def delete_person(uid):
    if uid not in data:
        return {"message": f"Person with ID {uid} not found"}, 404
    
    del data[uid]
    return {"message": f"Person with {uid} deleted"}, 200


# curl --header "Content-Type: application/json" -X POST -d '{"id": "124", "first_name": "Ferdy", "last_name": "Garrow", "country": "CanadaStates",}'  -i http://127.0.0.1:5000/persons/
# curl --header "Content-Type: application/json" -X POST --data "{'id': '124', 'first_name': 'Ferdy', 'last_name': 'Garrow', 'country': 'CanadaStates'}"  -i http://127.0.0.1:5000/persons

@app.route('/persons', methods=['POST'])
def add_person():
    print(request.data)
    print(request.json)
    new_person = request.get_json()
    print(type(new_person))

    if not new_person:
        return {"message": "Invalid input, no data provided"}, 422
    if 'id' in new_person:
        return {"message": "Invalid input, 'id' is set by server"}, 422

    new_id = None
    for i in range(5):
        new_id = random.randint(1,10000)
        new_id = str(new_id)
        if new_id not in data:
            break
    if not new_id:
        return {"message": "Not able to find a free id. Try again "}, 500
    

    try:
        data[new_id] = new_person
    except NameError:
        return {"message": "data not defined"}, 500

    return {"message": new_id}, 201



@app.errorhandler(404)
def api_not_found(error):
    return {'message':'API not found'}, 404



