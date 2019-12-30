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
    logging.info("Creating tables")
    db.create_all()


api.add_resource(Birthday, '/hello/<string:username>')


@app.route('/liveness')
def liveness_probe():
    return "ok", 200


if __name__ == '__main__':
    import logging
    from db import db

    logfile = os.environ.get('APP_LOG', 'app.log')
    logging.basicConfig(
        filename=logfile,
        level=logging.DEBUG
    )

    db.init_app(app)
    if os.environ.get('FLASK_DEBUG') == '1':
        flask_debug = True
    else:
        flask_debug = False

    logging.info("Application start..")
    app.run(port=os.environ.get('PORT', 5000), debug=flask_debug)
