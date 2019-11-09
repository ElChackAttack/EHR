from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(64), unique = True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    last_seen = db.Column(db.DateTime(), default = datetime.utcnow)
    creation_date = db.Column(db.DateTime(), default = datetime.utcnow)
    first_name = db.Column(db.String(64), unique = False, nullable = False)
    last_name = db.Column(db.String(64), unique = False, nullable = False)
    physicians = db.relationship('Physician', backref = 'user', lazy = True, passive_deletes=True)
    patient = db.relationship('Patient', backref = 'user', lazy = True, passive_deletes=True)
    Nurse = db.relationship('Nurse', backref = 'user', lazy = True, passive_deletes=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.unique_id'))

    def get_id(self):
        return self.user_id

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.user_id == current_app.config['FLASKY_ADMIN']:
                self.role_id = Role.query.filter_by(permissions=0xff).first()
            if self.role_id is None:
                self.role = Role.query.filter_by(default = True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.user_id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.user_id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.user_id

    def can(self, permissions):
        return self.role is not None and \
                (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Customer' : (Permission.BOOK_FLIGHTS, True),
            'Booking_agent' : (Permission.BOOK_FLIGHTS |
                                Permission.BOOK_FLIGHTS_FOR_OTHERS,
                                False),
            'Airline_staff' : (Permission.BOOK_FLIGHTS |
                                Permission.BOOK_FLIGHTS_FOR_OTHERS |
                                Permission.UPDATE_FLIGHTS,
                                False),
            'Administrator' : (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

class Permission:
    _USER_PERMISSION = 0x01
    _NURSE_PERMISSION = 0x02
    _PHYSICIAN_PERMISSION = 0x03

class Patient(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete = 'CASCADE'), primary_key = True)
    date_of_birth = db.Column(db.DateTime(), unique = False, nullable = False)
    SSN = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    insurance_id = db.Column(db.Integer, db.ForeignKey('insurance.insurance_id'))
    prescribed = db.relationship('Prescription', backref = 'patient', lazy = True)
    # appointments = db.relationship('Appointment', backref = 'patient', lazy = True)

    def get_id(self):
        return self.user_id

class Physician(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete = 'CASCADE'), primary_key = True)
    prescribed = db.relationship('Prescription', backref = 'physician', lazy = True)
    schedule = db.relationship('Physician_schedule', backref = 'physician', lazy = True)
    # appointments = db.relationship('Appointment', backref = 'patient', lazy = True)

    def get_id(self):
        return self.user_id

class Nurse(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete = 'CASCADE'), primary_key = True)

    def get_id(self):
        return self.user_id

class Insurance(db.Model):
    insurance_id = db.Column(db.Integer, primary_key = True)
    insurance_name = db.Column(db.String(128), nullable = False)
    subscribers = db.relationship('Patient', backref = 'insurance', lazy = True)

class Hospital(db.Model):
    unique_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable = False)
    user = db.relationship('User', backref = 'hospital', lazy = True)

class Facility(db.Model):
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.unique_id'), primary_key = True, unique = False, index = True)
    facility_num = db.Column(db.String(64), primary_key = True, unique = False, index = True)
    #appointment_hospital = db.relationship('Appointment', foreign_keys = 'Appointment.hospital_id', backref = 'facility', lazy = True)
    #appointment_facility = db.relationship('Appointment', foreign_keys = 'Appointment.facility_num', backref = 'facility', lazy = True)

class Appointment(db.Model):
    appointment_id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.user_id'), nullable = False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('facility.hospital_id'), nullable = False)
    facility_num = db.Column(db.String(64), db.ForeignKey('facility.facility_num'), nullable = False)
    event_id = db.Column(db.Integer, db.ForeignKey('physician_schedule.event_id'), nullable = False)
    notes = db.Column(db.Text, nullable = True)
    hospital_id_rel = db.relationship("Facility", foreign_keys=[hospital_id])
    facility_num_rel = db.relationship("Facility", foreign_keys=[facility_num])

class Prescription(db.Model):
    prescription_id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.user_id'), nullable = False)
    physician_id = db.Column(db.Integer, db.ForeignKey('physician.user_id'), nullable = False)
    date_prescribed = db.Column(db.Date, nullable = False)
    expir_date = db.Column(db.Date, nullable = False)
    description = db.Column(db.Text, nullable = True)

class Physician_schedule(db.Model):
    event_id = db.Column(db.Integer, primary_key = True)
    physician_id = db.Column(db.Integer, db.ForeignKey('physician.user_id'), nullable = False)
    start_time = db.Column(db.DateTime, nullable = False)
    end_time = db.Column(db.DateTime, nullable = False)
    event_type = db.Column(db.String(64), nullable = False)
    appointments = db.relationship("Appointment", backref = 'physician_schedule', lazy = True)
