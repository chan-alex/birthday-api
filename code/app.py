import os
from flask import Flask
from flask_restful import Api
from Resources import Birthday


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = \
    os.environ.get('DATABASE_URI', 'sqlite:///data.db')
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Birthday, '/hello/<string:username>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    if os.environ.get('FLASK_DEBUG') == '1':
        flask_debug = True
    else:
        flask_debug = False
    app.run(port=os.environ.get('PORT', 5000), debug=flask_debug)
