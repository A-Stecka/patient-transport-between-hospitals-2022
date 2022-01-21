from faker import Faker
from random import *

from constants import *
from models import *

fake = Faker()

# users
users = []
adm_employees = []
doctors = []
medics = []
drivers = []
supervisors = []
administrators = []

# other
vehicles = []
locations = []
medical_facilities = []
hospital_wards = []
patients = []
transfers = []
medical_exams = []
referrals = []


# methods used to check if value is unique

def get_logins():
    all_users = User.nodes.all()
    return [single_user.login for single_user in all_users]


def get_license_plates():
    all_vehicles = Vehicle.nodes.all()
    return [single_vehicle.license_plate for single_vehicle in all_vehicles]


# method to get all users used when generating relationships

def get_users():
    return User.nodes.all()


# nodes

def generate_adm_employees():
    logins = get_logins()
    for i in range(0, ADM_EMPLOYEE_LIMIT):
        login = fake.user_name()
        while logins.count(login) != 0:
            login = fake.user_name()
        logins.append(login)
        new_user = AdmEmployee(
            login=login,
            password=fake.password(),
            name=fake.first_name(),
            surname=fake.last_name())
        new_user.save()
        adm_employees.append(new_user)


def generate_doctors():
    logins = get_logins()
    for i in range(0, DOCTORS_LIMIT):
        login = fake.user_name()
        while logins.count(login) != 0:
            login = fake.user_name()
        logins.append(login)
        new_user = Doctor(
            login=login,
            password=fake.password(),
            name=fake.first_name(),
            surname=fake.last_name())
        new_user.save()
        doctors.append(new_user)


def generate_medics():
    logins = get_logins()
    for i in range(0, MEDICS_LIMIT):
        login = fake.user_name()
        while logins.count(login) != 0:
            login = fake.user_name()
        logins.append(login)
        new_user = Medic(
            login=login,
            password=fake.password(),
            name=fake.first_name(),
            surname=fake.last_name())
        new_user.save()
        medics.append(new_user)


def generate_drivers():
    logins = get_logins()
    for i in range(0, DRIVERS_LIMIT):
        login = fake.user_name()
        while logins.count(login) != 0:
            login = fake.user_name()
        logins.append(login)
        new_user = Driver(
            login=login,
            password=fake.password(),
            name=fake.first_name(),
            surname=fake.last_name())
        new_user.save()
        drivers.append(new_user)


def generate_supervisors():
    logins = get_logins()
    for i in range(0, SUPERVISORS_LIMIT):
        login = fake.user_name()
        while logins.count(login) != 0:
            login = fake.user_name()
        logins.append(login)
        new_user = Supervisor(
            login=login,
            password=fake.password(),
            name=fake.first_name(),
            surname=fake.last_name())
        new_user.save()
        supervisors.append(new_user)


def generate_administrators():
    logins = get_logins()
    for i in range(0, ADMINISTRATORS_LIMIT):
        login = fake.user_name()
        while logins.count(login) != 0:
            login = fake.user_name()
        logins.append(login)
        new_user = Administrator(
            login=login,
            password=fake.password(),
            name=fake.first_name(),
            surname=fake.last_name())
        new_user.save()
        administrators.append(new_user)


def generate_locations():
    for i in range(0, LOCATIONS_LIMIT):
        location = Location(
            city=fake.city(),
            address=fake.street_address(),
            postalCode=randint(POSTAL_CODE_LOWER_LIMIT, POSTAL_CODE_UPPER_LIMIT)
        )
        location.save()
        locations.append(location)


def generate_medical_facilities():
    for i in range(0, MEDICAL_FACILITIES_LIMIT):
        medical_facility = MedicalFacility(
            name=fake.pystr()
        )
        medical_facility.save()
        medical_facilities.append(medical_facility)


def generate_hospital_wards():
    for i in range(0, HOSPITAL_WARDS_LIMIT):
        hospital_ward = choice(HOSPITAL_WARDS)
        hospital_ward = HospitalWard(
            name=hospital_ward,
            places=randint(0, PLACES_IN_WARD_LIMIT)
        )
        hospital_ward.save()
        hospital_wards.append(hospital_ward)


def generate_vehicles():
    license_plates = get_license_plates()
    for i in range(0, VEHICLES_LIMIT):
        license_plate = fake.license_plate()
        while license_plates.count(license_plate) != 0:
            license_plate = fake.license_plate()
        license_plates.append(license_plate)
        seats = int(choice(SEATS))
        vehicle = Vehicle(
            brand=fake.pystr(2, 20),
            model=fake.pystr(3, 20),
            licensePlate=license_plate,
            seats=seats
        )
        vehicle.save()
        vehicles.append(vehicle)


def generate_transfers():
    for i in range(0, TRANSFERS_LIMIT):
        start_date = fake.date_between(start_date=START_DATE, end_date='+1y')
        transfer = Transfer(
            startTime=fake.time(),
            startDate=start_date,
            status=choice(TRANSFER_STATUS),
            valid=fake.date_between(start_date=START_DATE, end_date=start_date)
        )
        transfer.save()
        transfers.append(transfer)


def generate_patients():
    for i in range(0, PATIENTS_LIMIT):
        patient = Patient(
            name=fake.first_name(),
            surname=fake.last_name()
        )
        patient.save()
        patients.append(patient)


def generate_referrals():
    for i in range(0, REFERRALS_LIMIT):
        body_parts = None
        if fake.pybool():
            body_parts = choice(BODY_PARTS)
        referral = Referral(
            referralDate=fake.date_between(START_DATE, END_DATE),
            bodyPart=body_parts
        )
        referral.save()
        referrals.append(referral)


def generate_medical_exams():
    for i in range(0, MEDICAL_EXAMS_LIMIT):
        medical_exam = MedicalExam(
            name=fake.pystr(5, 45),
        )
        medical_exam.save()
        medical_exams.append(medical_exam)


# relationships

def generate_executed_by():
    for transfer in transfers:
        driver = choice(drivers)
        transfer.driver.connect(driver)


def generate_books():
    for transfer in transfers:
        vehicle = choice(vehicles)
        transfer.vehicle.connect(vehicle)


def generate_is_from():
    for transfer in transfers:
        medical_facility = choice(medical_facilities)
        transfer.medicalFacilityFrom.connect(medical_facility)


def generate_is_to():
    for transfer in transfers:
        medical_facility = choice(medical_facilities)
        transfer.medicalFacilityTo.connect(medical_facility)


def generate_overseen_by():
    for transfer in transfers:
        medics_quantity = randint(0, MEDICS_IN_TRANSFER_LIMIT)
        for x in range(medics_quantity):
            medic = choice(medics)
            transfer.medic.connect(medic)


def generate_works():
    for user in get_users():
        medical_facility = choice(medical_facilities)
        user.medicalFacility.connect(medical_facility)


def generate_manages():
    for supervisor in supervisors:
        medical_facility = choice(medical_facilities)
        supervisor.medicalFacility.connect(medical_facility)


def generate_creates():
    for administrator in administrators:
        supervisor = choice(supervisors)
        administrator.supervisor.connect(supervisor)


def generate_owns():
    for medical_facility in medical_facilities:
        wards_quantity = randint(0, WARDS_IN_FACILITY_LIMIT)
        for x in range(wards_quantity):
            hospital_ward = choice(hospital_wards)
            medical_facility.hospitalWard.connect(hospital_ward)


def generate_offers():
    for medical_facility in medical_facilities:
        medical_exam = choice(medical_exams)
        medical_facility.medicalExam.connect(medical_exam, {'limit': randint(0, DAILY_LIMIT_LIMIT)})
    for i in range(OFFERS_LIMIT - MEDICAL_FACILITIES_LIMIT):
        medical_exam = choice(medical_exams)
        medical_facility = choice(medical_facilities)
        medical_facility.medicalExam.connect(medical_exam, {'limit': randint(0, DAILY_LIMIT_LIMIT)})


def generate_is_occupied_occupies_place():
    for patient in patients:
        admission_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
        discharge_date = fake.date_between(start_date=START_DATE, end_date='+1y')
        hospital_ward = choice(hospital_wards)
        if choice([True, False]):
            patient.hospitalWard.connect(hospital_ward, {'admissionDate': admission_date, 'dischargeDate': discharge_date})
            hospital_ward.patient.connect(patient, {'admissionDate': admission_date, 'dischargeDate': discharge_date})
        else:
            patient.hospitalWard.connect(hospital_ward, {'admissionDate': admission_date})
            hospital_ward.patient.connect(patient, {'admissionDate': admission_date})

    for i in range(IS_OCCUPIED_LIMIT - PATIENTS_LIMIT):
        patient = choice(patients)
        admission_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
        discharge_date = fake.date_between(start_date=START_DATE, end_date='+1y')
        hospital_ward = choice(hospital_wards)
        if choice([True, False]):
            patient.hospitalWard.connect(hospital_ward, {'admissionDate': admission_date, 'dischargeDate': discharge_date})
            hospital_ward.patient.connect(patient, {'admissionDate': admission_date, 'dischargeDate': discharge_date})
        else:
            patient.hospitalWard.connect(hospital_ward, {'admissionDate': admission_date})
            hospital_ward.patient.connect(patient, {'admissionDate': admission_date})


def generate_belongs_to_has():
    for vehicle in vehicles:
        medical_facility = choice(medical_facilities)
        vehicle.medicalFacility.connect(medical_facility)
        medical_facility.vehicle.connect(vehicle)


def generate_participates():
    for patient in patients:
        transfer_quantity = randint(0, PARTICIPATES_LIMIT)
        for x in range(transfer_quantity):
            transfer = choice(transfers)
            patient.transfer.connect(transfer, {'status': choice(STATUS)})


def generate_gets():
    for referral in referrals:
        patients_quantity = randint(0, GETS_LIMIT)
        for x in range(patients_quantity):
            patient = choice(patients)
            referral.patient.connect(patient)


def generate_issued_by():
    for referral in referrals:
        doctor = choice(doctors)
        referral.doctor.connect(doctor)


def generate_concerns():
    for referral in referrals:
        medical_exam = choice(medical_exams)
        referral.medicalExam.connect(medical_exam)


def generate_is_reserved():
    for patient in patients:
        start_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
        start_time = fake.time()
        medical_exam = choice(medical_exams)
        medical_exam.patient.connect(patient, {"startDate": start_date, "startTime": start_time})


def generate_is_in():
    for medical_facility in medical_facilities:
        location = choice(locations)
        medical_facility.location.connect(location)


