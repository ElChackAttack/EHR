#the relationship is established with db.relationship()
#where the backref, specifies the reverse direction of the relationship
#in adding the backreference, you can access the relational model as an object
#rather than a list etc.

from . import db

class Physician(db.Model):
    __tablename__ = 'Physician'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False, nullable = False)
    last_name = db.Column(db.String(64), unique=False, nullable = False)
    email = db.Column(db.String(64), unique=True, nullable = False)
    password = db.Column(db.String(64), unique = False, nullable = False)
    patients = db.relationship('Patient', backref = 'physician')
    prescriptions_issued = db.relationship('Prescription')
    appointments = db.relationship('Appointment')
    hospital = db.Column(db.Integer, db.ForeignKey('Hospital.id'))
    def __repr__(self):
        return '<Physician %r>' % self.first_name

class Patient(db.Model):
    __tablename__ = 'Patient'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False, nullable = False)
    last_name = db.Column(db.String(64), unique=False, nullable = False)
    email = db.Column(db.String(64), unique = True, nullable = False)
    password = db.Column(db.String(64), unique = False, nullable = False)
    ssn = db.Column(db.Integer, unique = True, nullable = False)
    dob = db.Column(db.DateTime)
    physician_id = db.Column(db.Integer, db.ForeignKey('Physician.id'))
    prescriptions = db.relationship('Prescription', backref = 'prescribed')
    appointments = db.relationship('Appointment', backref = 'patient')

    def __repr__(self):
        return '<Patient %r>' % self.first_name

class Prescription(db.Model):
    __tablename__ = 'Prescription'
    medication = db.Column(db.String(64), unique = False, nullable = False, primary_key = True)
    date_prescribed = db.Column(db.DateTime, unique = False, nullable = False, primary_key = True)
    date_expired = db.Column(db.DateTime, unique = False, nullable = False)
    description = db.Column(db.Text, unique = False, nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'), primary_key = True)
    physician_id = db.Column(db.Integer, db.ForeignKey('Physician.id'), primary_key = True)

    def __repr__(self):
        return '<Prescription %r>' % self.medication

class Appointment(db.Model):
    __tablename__ = 'Appointment'
    appointment_id = db.Column(db.Integer, primary_key = True)
    start_time = db.Column(db.DateTime, unique = False, nullable = False)
    end_time = db.Column(db.DateTime, unique = False, nullable = False)
    physician_id = db.Column(db.Integer, db.ForeignKey('Physician.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'))

    def __repr__(self):
        return '<Appointment %r>' % self.appointment_id

class Room(db.Model):
    __tablename__ = 'Room'
    room_number = db.Column(db.Integer, primary_key = True)
    building = db.Column(db.String(64), unique = False, nullable = False)
    hospital = db.Column(db.Integer, db.ForeignKey('Hospital.id'))


    def __repr__(self):
        return '<Room %r>' % self.room_number

class Hospital(db.Model):
    __tablename__ = 'Hospital'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)
    country = db.Column(db.String(64), unique = False, nullable = False)
    state = db.Column(db.String(64), unique = False, nullable = False)
    city = db.Column(db.String(64), unique = False, nullable = False)
    zipcode = db.Column(db.String(64), unique = False, nullable = False)
    rooms = db.relationship('Room')
    physicians = db.relationship('Physician')

    def __repr__(self):
        return '<Hospital %r>' % self.name
