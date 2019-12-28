import json, datetime
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from Models import BirthdayModel


app = Flask(__name__)
api = Api(app)


class Birthday(Resource):

    def get(self, username):
        return { "message": "Hello, {}. Your birthday is in N days".format(username) }


    def put(self, username):

        if BirthdayModel.valid_username(username) == False:
            return { "message": "User name should contain alphabets only" }, 422  # return for easier testing.

        parser = reqparse.RequestParser()
        parser.add_argument( 'dateOfBirth',
                type=str,
                required=True,
                help="This field cannot be left blank",
        )
        json_payload = parser.parse_args()
        dob = json_payload['dateOfBirth']
        if BirthdayModel.valid_dob(dob) == False:
            return { "message": "dateOfBirth should be in YYYY-MM-DD" }, 400  # return for easier testing.

        return "", 204


api.add_resource(Birthday, '/hello/<string:username>')

app.run(port=5000, debug=True)    
