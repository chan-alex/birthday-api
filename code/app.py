from flask import Flask, request, jsonify
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class Birthday(Resource):
    def get(self, name):
        return { "message": "Hello, {}. Your birthday is in N days".format(name)}

    def put(self, name):
        request_data = request.get_json(force=True) # force=True relax content-type requirement
        return request_data


api.add_resource(Birthday, '/hello/<string:name>')

app.run(port=5000, debug=True)    
