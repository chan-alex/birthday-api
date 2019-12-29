import logging
from flask_restful import Resource, reqparse
from Models import BirthdayModel


class Birthday(Resource):

    def get(self, username):
        if BirthdayModel.valid_username(username) is False:
            logging.debug("GET method: invalid username = {}. Rejecting.".format(username))
            return {"message": "User name should contain alphabets only"}, 422  # return for easier testing.

        days = BirthdayModel.days_till_birthday(username)
        if days == 0:
            return {"message": "Hello, {}! Happy birthday!".format(username)}
        elif days is not None:
            return {"message": "Hello, {}. Your birthday is in {} days".format(username, days)}

    def put(self, username):
        if BirthdayModel.valid_username(username) is False:
            logging.debug("GET method: invalid username = {}. Rejecting.".format(username))
            return {"message": "User name should contain alphabets only"}, 422  # return for easier testing.

        parser = reqparse.RequestParser()
        parser.add_argument('dateOfBirth',
                            type=str,
                            required=True,
                            help="This field cannot be left blank"
                            )
        json_payload = parser.parse_args()
        dob = json_payload['dateOfBirth']
        if BirthdayModel.valid_dob(dob) is False:
            logging.debug("GET method: invalid DOB = {}. Rejecting.".format(dob))
            return {"message": "dateOfBirth should be in YYYY-MM-DD"}, 400  # return for easier testing.

        birthday = BirthdayModel(username, dob)
        birthday.save_to_db()
        logging.debug("Saving username = {}".format(username))

        return "", 204
