from neomodel import *


class User(StructuredNode):
    login = StringProperty()
    name = StringProperty()
    surname = StringProperty()
    password = StringProperty()

    medicalFacility = RelationshipTo('MedicalFacility', "WORKS")


class AdmEmployee(User):
    pass


class Doctor(User):
    pass


class Medic(User):
    pass


class Driver(User):
    pass


class Supervisor(User):
    medicalFacility = RelationshipTo('MedicalFacility', 'MANAGES')


class Administrator(User):
    supervisor = RelationshipTo('Supervisor', 'CREATES')


class Location(StructuredNode):
    adress = StringProperty()
    city = StringProperty()
    postalCode = StringProperty()


class OffersRel(StructuredRel):
    limit = IntegerProperty()


class MedicalFacility(StructuredNode):
    name = StringProperty()

    location = RelationshipTo('Location', 'IS_IN')
    hospitalWard = RelationshipTo('HospitalWard', 'OWNS')
    vehicle = RelationshipTo('Vehicle', 'HAS')
    medicalExam = RelationshipTo('MedicalExam', 'OFFERS', model=OffersRel)


class IsOccupiedRel(StructuredRel):
    admissionDate = StringProperty()
    dischargeDate = StringProperty()


class HospitalWard(StructuredNode):
    name = StringProperty()
    places = IntegerProperty()

    patient = RelationshipTo('Patient', 'IS_OCCUPIED', model=IsOccupiedRel)


class Vehicle(StructuredNode):
    brand = StringProperty()
    licensePlate = StringProperty()
    model = StringProperty()
    seats = IntegerProperty()

    medicalFacility = RelationshipTo('MedicalFacility', 'BELONGS_TO')


class Transfer(StructuredNode):
    startTime = StringProperty()
    startDate = StringProperty()
    status = StringProperty()
    valid = StringProperty()

    driver = RelationshipTo('Driver', 'EXECUTED_BY')
    vehicle = RelationshipTo('Vehicle', 'BOOKS')
    historyTransfer = RelationshipFrom('Transfer', 'PREVIOUS')
    medicalFacilityFrom = RelationshipTo('MedicalFacility', 'IS_FROM')
    medicalFacilityTo = RelationshipTo('MedicalFacility', 'IS_TO')
    medic = RelationshipTo('Medic', 'OVERSEEN_BY')


class OccupiesPlaceRel(StructuredRel):
    admissionDate = StringProperty()
    dischargeDate = StringProperty()


class ParticipatesRel(StructuredRel):
    status = StringProperty()


class Patient(StructuredNode):
    name = StringProperty()
    surname = StringProperty()

    hospitalWard = RelationshipTo('HospitalWard', 'OCCUPIES_PLACE', model=OccupiesPlaceRel)
    transfer = RelationshipTo('Transfer', 'PARTICIPATES', model=ParticipatesRel)


class Referral(StructuredNode):
    bodyPart = StringProperty()
    referralDate = StringProperty()

    patient = RelationshipFrom('Patient', 'GETS')
    doctor = RelationshipTo('Doctor', 'ISSUED_BY')
    medicalExam = RelationshipTo('MedicalExam', 'CONCERNS')


class IsReservedRel(StructuredRel):
    startDate = StringProperty()
    startTime = StringProperty()


class MedicalExam(StructuredNode):
    name = StringProperty()

    patient = RelationshipTo('Patient', "IS_RESERVED", model=IsReservedRel)
