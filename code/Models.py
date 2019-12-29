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


    def __str__(self):
        return 'name = {self.username}, dob = {self.dateOfBirth}'.format(self=self)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def days_till_birthday(cls, name):
        query_result = BirthdayModel.find_by_username(name)

        if query_result == None:
            return None

        dob = datetime.datetime.strptime(query_result.dateOfBirth, '%Y-%m-%d')
        dob_month = dob.month
        dob_day = dob.day

        today = datetime.datetime.now()
        # ensure start from 0000hrs.
        today = datetime.datetime(today.year, today.month, today.day)

        this_year_dob = datetime.datetime(today.year, dob_month, dob_day)
        next_year_dob = datetime.datetime(today.year+1, dob_month, dob_day)

        if today == this_year_dob:
            return 0
        elif today < this_year_dob:
            return (this_year_dob - today).days
        else:
            return (next_year_dob - today).days



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
