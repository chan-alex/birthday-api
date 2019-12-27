from flask import Flask, request, jsonify
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class Birthday(Resource):

    def get(self, username):
        return { "message": "Hello, {}. Your birthday is in N days".format(username) }


    def put(self, username):
        # Check if supplied user name contains only letters.
        if username.isalpha() == False:
            return { "message": "User name should contain alphabets only" }, 422  # return for easier testing.

        request_data = request.get_json(force=True) # force=True relax content-type requirement
        return "", 204


api.add_resource(Birthday, '/hello/<string:username>')

app.run(port=5000, debug=True)    
