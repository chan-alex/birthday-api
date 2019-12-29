import json, datetime
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from Models import BirthdayModel


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


class Birthday(Resource):

    def get(self, username):
        if BirthdayModel.valid_username(username) == False:
            return { "message": "User name should contain alphabets only" }, 422  # return for easier testing.

        days = BirthdayModel.days_till_birthday(username)
        if days == 0:
            return { "message": "Hello, {}! Happy birthday!".format(username) }
        elif days != None:
            return { "message": "Hello, {}. Your birthday is in {} days".format(username, days) }


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

        birthday = BirthdayModel(username,dob)
        birthday.save_to_db()

        return "", 204


api.add_resource(Birthday, '/hello/<string:username>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)    
