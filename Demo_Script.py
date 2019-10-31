from app.models import *


def main():
    saint_jude = Hospital(name = 'Saint Jude', country = 'U.S.', state = 'NJ',
                    city = 'Elizabeth', zipcode = '08820')
    alex = Physician(first_name = 'Alex',last_name = 'Bog',email = 'alexkbog@gmail.com',
                    password = 'abc', hospital = saint_jude)



if __name__ == '__main__':
    main()

    #
    # id = db.Column(db.Integer, primary_key=True)
    # first_name = db.Column(db.String(64), unique=False, nullable = False)
    # last_name = db.Column(db.String(64), unique=False, nullable = False)
    # email = db.Column(db.String(64), unique = True, nullable = False)
    # password = db.Column(db.String(64), unique = False, nullable = False)
    # ssn = db.Column(db.Integer, unique = True, nullable = False)
    # dob = db.Column(db.DateTime)
    # physician_id = db.Column(db.Integer, db.ForeignKey('physician.id'))
    # prescriptions = db.relationship('prescription', backref = 'prescribed')
    # appointments = db.relationship('appointment', backref = 'patient')
