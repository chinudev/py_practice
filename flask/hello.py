#  flask --app <this-file> --debug run 
# test using : curl -i http://127.0.0.1:5000/<path> 

from flask import Flask, make_response, request

app = Flask(__name__) 

@app.route("/")
def index():
    return "<b>hello world</b>\n"

# Return status code explicitly
@app.route('/no_content')
def no_content():
    return ({'message': 'Absolutely no content found'}, 204)


# Use response object directly
@app.route('/exp')
def index_explicit():
    resp = make_response({'name' : 'Tom', 'age' : 23})
    resp.status_code = 200
    return resp 

# You can access the query parameters from the immutable dictionary
#  stored in request.args
@app.route('/query')
def query():
    if not request.args:
        return { 'message': 'No query parameters provided. example: base-url/query?q=3&a=apple'}, 400

    return {'message': 'Query params are ' + str(request.args)}

