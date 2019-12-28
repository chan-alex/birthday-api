import datetime


class BirthdayModel:
    def __init__(self, name, dob):
        self.name = name
        self.dob = dob
    
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

