import datetime
from db import db


class BirthdayModel(db.Model):
    __tablename__ = 'birthdays'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    dateOfBirth = db.Column(db.String(10))


    def __init__(self, username, dob):
        self.username = username
        self.dateOfBirth = dob


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def valid_username(cls, name):
        return name.isalpha() == True


    @classmethod
    def valid_dob(cls, dob):
        try:
            dob = datetime.datetime.strptime(dob, '%Y-%m-%d')
        except Exception as e:
            print(e)
            return False
        return True


    @classmethod
    def find_by_username(cls, name):
        return cls.query.filter_by(username=name).first()
