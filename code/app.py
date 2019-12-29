import json, datetime
from flask import Flask, request, jsonify
from flask_restful import Api
from Models import BirthdayModel
from Resources import Birthday


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Birthday, '/hello/<string:username>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)    
