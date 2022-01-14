from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'

    Id_user = Column(Integer, primary_key=True)
    Login = Column(String)
    Password = Column(String)
    Name = Column(String)
    Surname = Column(String)

    roles = relationship('Roles', backref='users')
    medical_facilities = relationship('Medical_facilities', backref='users')
    transfers = relationship('Transfers', backref='users')
    referrals = relationship('Referrals', backref='users')
    employments = relationship('Employments', backref='users')
    users_transfers = relationship('Users_Transfers', backref='users')


class Locations(Base):
    __tablename__ = 'Locations'

    Id_location = Column(Integer, primary_key=True, autoincrement=True)
    City = Column(String)
    Address = Column(String)
    Postal_code = Column(String)

    medical_facilities = relationship('Medical_facilities', backref='locations')


class Medical_facilities(Base):
    __tablename__ = 'Medical_facilities'

    Id_medical_facility = Column(Integer, primary_key=True,  autoincrement=True)
    Name = Column(String)
    FK_location = Column(Integer, ForeignKey('Locations.Id_location'))
    FK_user = Column(Integer, ForeignKey('Users.Id_user'))

    hospital_wards = relationship('Hospital_wards', backref='medical_facilities')
    employments = relationship('Employments', backref='medical_facilities')
    exam_offers = relationship('Exam_offers', backref='medical_facilities')
    transfers = relationship('Transfers', backref='medical_facilities')


class Hospital_wards(Base):
    __tablename__ = 'Hospital_wards'

    Id_hospital_ward = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Places = Column(Integer)
    FK_medical_facility = Column(Integer, ForeignKey('Medical_facilities.Id_medical_facility'))

    admissions = relationship('Admissions', backref='hospital_wards')


class Vehicles(Base):
    __tablename__ = 'Vehicles'

    Id_vehicle = Column(Integer, primary_key=True, autoincrement=True)
    Brand = Column(String)
    Model = Column(String)
    License_plate = Column(String)
    Seats = Column(Integer)
    FK_medical_facility = Column(Integer, ForeignKey('Medical_facilities.Id_medical_facility'))

    transfers = relationship('Transfers', backref='vehicles')


class Transfers(Base):
    __tablename__ = 'Transfers'

    Id_transfer = Column(Integer, primary_key=True,  autoincrement=True)
    Start_time = Column(Time)
    Start_date = Column(Date)
    FK_user = Column(Integer, ForeignKey('Users.Id_user'))
    FK_vehicle = Column(Integer, ForeignKey('Vehicles.Id_vehicle'))
    FK_facility_from = Column(Integer, ForeignKey('Medical_facilities.Id_medical_facility'))
    FK_facility_to = Column(Integer, ForeignKey('Medical_facilities.Id_medical_facility'))

    passengers = relationship('Passengers', backref='transfers')
    users_transfers = relationship('Users_Transfers', backref='transfers')


class Roles(Base):
    __tablename__ = 'Roles'

    Id_role = Column(Integer, primary_key=True,  autoincrement=True)
    FK_user = Column(Integer, ForeignKey('Users.Id_user'))
    Name = Column(String)
    unique_together = ('FK_user', 'Name')


class Patients(Base):
    __tablename__ = 'Patients'

    Id_patient = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Surname = Column(String)

    reservations = relationship('Reservations', backref='patients')
    admissions = relationship('Admissions', backref='patients')
    referrals = relationship('Referrals', backref='patients')
    passengers = relationship('Passengers', backref='patients')


class Admissions(Base):
    __tablename__ = 'Admissions'

    Id_admission = Column(Integer, primary_key=True, autoincrement=True)
    FK_hospital_ward = Column(Integer, ForeignKey('Hospital_wards.Id_hospital_ward'))
    FK_patient = Column(Integer, ForeignKey('Patients.Id_patient'))
    Admission_date = Column(Date)
    Discharge_date = Column(Date, nullable=True)


class Referrals(Base):
    __tablename__ = 'Referrals'

    Id_referral = Column(Integer, primary_key=True, autoincrement=True)
    FK_user = Column(Integer, ForeignKey('Users.Id_user'))
    FK_patient = Column(Integer, ForeignKey('Patients.Id_patient'))
    Referral_date = Column(Date)
    Body_part = Column(String, nullable=True)

    referrals_medical_exams = relationship('Referrals_Medical_exams', backref='referrals')


class Medical_exams(Base):
    __tablename__ = 'Medical_exams'

    Id_medical_exam = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)

    reservations = relationship('Reservations', backref='medical_exams')
    exam_offers = relationship('Exam_offers', backref='medical_exams')
    referrals_medical_exams = relationship('Referrals_Medical_exams', backref='medical_exams')


class Reservations(Base):
    __tablename__ = 'Reservations'

    Id_reservaion = Column(Integer, primary_key=True, autoincrement=True)
    Start_date = Column(Date)
    Start_time = Column(Time)
    FK_patient = Column(Integer, ForeignKey('Patients.Id_patient'))
    FK_medical_exam = Column(Integer, ForeignKey('Medical_exams.Id_medical_exam'))


class Exam_offers(Base):
    __tablename__ = 'Exam_offers'

    Id_exam_offers = Column(Integer, primary_key=True, autoincrement=True)
    FK_medical_facility = Column(Integer, ForeignKey('Medical_facilities.Id_medical_facility'))
    FK_medical_exam = Column(Integer, ForeignKey('Medical_exams.Id_medical_exam'))
    Daily_limit = Column(Integer, nullable=True)


class Employments(Base):
    __tablename__ = 'Employments'

    Id_employment = Column(Integer, primary_key=True, autoincrement=True)
    FK_medical_facility = Column(Integer, ForeignKey('Medical_facilities.Id_medical_facility'))
    FK_user = Column(Integer, ForeignKey('Users.Id_user'))
    Employment_date = Column(Date)
    Dismissal_date = Column(Date, nullable=True)


class Passengers(Base):
    __tablename__ = 'Passengers'

    Id_passenger = Column(Integer, primary_key=True, autoincrement=True)
    FK_patient = Column(Integer, ForeignKey('Patients.Id_patient'))
    FK_transfer = Column(Integer, ForeignKey('Transfers.Id_transfer'))
    Needs_care = Column(String)
    Status = Column(String)


class Referrals_Medical_exams(Base):
    __tablename__ = 'Refferals_Medical_exams'

    Id_ref_med = Column(Integer, primary_key=True, autoincrement=True)
    FK_medical_exam = Column(Integer, ForeignKey('Medical_exams.Id_medical_exam'))
    FK_referral = Column(Integer, ForeignKey('Referrals.Id_referral'))


class Users_Transfers(Base):
    __tablename__ = 'Users_Transfers'

    Id_user_transfer = Column(Integer, primary_key=True, autoincrement=True)
    FK_user = Column(Integer, ForeignKey('Users.Id_user'))
    FK_transfer = Column(Integer, ForeignKey('Transfers.Id_transfer'))
