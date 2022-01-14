from random import *

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from constants import *
from tables import *

fake = Faker()

user = 'root'
pwd = 'root123'
host = 'localhost'
db = 'medical_transport'
mysql_engine = create_engine('mysql://{0}:{1}@{2}/{3}'.format(user, pwd, host, db))

Session = sessionmaker(bind=mysql_engine)
session = Session()


def get_logins(session):
    return [user.Login for user in session.query(Users).all()]


def get_supervisors(session):
    return [medical_facility.FK_user for medical_facility in session.query(Medical_facilities).all()]


def get_license_plates(session):
    return [vehicle.License_plate for vehicle in session.query(Vehicles).all()]


def get_hospital_wards(session):
    return [(hospital_ward.Name, hospital_ward.FK_medical_facility)
            for hospital_ward in session.query(Hospital_wards).all()]


def get_users_with_role(session, role_id):
    users = session.query(Roles).all()
    users_with_role = []
    for user in users:
        if user.Name == ROLES[role_id]:
            users_with_role.append(user.FK_user)
    return users_with_role


def generate_users(session):
    logins = get_logins(session)
    for i in range(0, USERS_LIMIT):
        login = fake.user_name()
        while logins.count(login) != 0:
            login = fake.user_name()
        logins.append(login)
        new_user = Users(
            Login=login,
            Password=fake.password(),
            Name=fake.first_name(),
            Surname=fake.last_name()
        )
        session.add(new_user)
    session.commit()


def generate_roles(session):
    user_index = 1
    for i in range(0, MEDICAL_FACILITIES_LIMIT):
        role = Roles(
            FK_user=user_index,
            Name=ROLES[1]
        )
        user_index = user_index + 1
        session.add(role)
    for i in range(0, min(USERS_LIMIT - MEDICAL_FACILITIES_LIMIT, ROLES_LIMIT)):
        role = Roles(
            FK_user=user_index,
            Name=choice(ROLES)
        )
        user_index = user_index + 1
        session.add(role)
    for i in range(0, ROLES_LIMIT - USERS_LIMIT):
        role = Roles(
            FK_user=randint(1, USERS_LIMIT),
            Name=choice(ROLES)
        )
        session.add(role)
    session.commit()


def generate_locations(session):
    for i in range(0, LOCATIONS_LIMIT):
        location = Locations(
            City=fake.city(),
            Address=fake.street_address(),
            Postal_code=randint(POSTAL_CODE_LOWER_LIMIT, POSTAL_CODE_UPPER_LIMIT)
        )
        session.add(location)
    session.commit()


def generate_medical_facilities(session):
    supervisors = get_supervisors(session)
    possible_supervisors = get_users_with_role(session, 1)
    for i in range(0, MEDICAL_FACILITIES_LIMIT):
        supervisor = choice(possible_supervisors)
        while supervisors.count(supervisor) != 0:
            supervisor = choice(possible_supervisors)
        supervisors.append(supervisor)
        medical_facility = Medical_facilities(
            Name=fake.pystr(),
            FK_location=randint(1, MEDICAL_FACILITIES_LIMIT),
            FK_user=supervisor
        )
        session.add(medical_facility)
    session.commit()


def generate_hospital_wards(session):
    hospital_wards = []
    for i in range(0, HOSPITAL_WARDS_LIMIT):
        medical_facility = randint(1, MEDICAL_FACILITIES_LIMIT)
        hospital_ward = choice(HOSPITAL_WARDS)
        while hospital_wards.count([hospital_ward, medical_facility]) != 0:
            hospital_ward = choice(HOSPITAL_WARDS)
        hospital_ward_A = Hospital_wards(
            Name=hospital_ward,
            Places=randint(0, PLACES_IN_WARD_LIMIT),
            FK_medical_facility=medical_facility
        )
        hospital_wards.append([hospital_ward, medical_facility])
        session.add(hospital_ward_A)
    session.commit()


def generate_vehicles(session):
    license_plates = get_license_plates(session)
    for i in range(0, VEHICLES_LIMIT):
        license_plate = fake.license_plate()
        while license_plates.count(license_plate) != 0:
            license_plate = fake.license_plate()
        license_plates.append(license_plate)
        seats = int(choice(SEATS))
        vehicle = Vehicles(
            Brand=fake.pystr(2, 20),
            Model=fake.pystr(3, 20),
            License_plate=license_plate,
            Seats=seats,
            FK_medical_facility=randint(1, MEDICAL_FACILITIES_LIMIT)
        )
        session.add(vehicle)
    session.commit()


def generate_transfers(session):
    possible_drivers = get_users_with_role(session, 3)
    for i in range(0, TRANSFERS_LIMIT):
        transfer = Transfers(
            Start_time=fake.time(),
            Start_date=fake.date_between(start_date=START_DATE, end_date='+1y'),
            FK_user=choice(possible_drivers),
            FK_vehicle=randint(1, VEHICLES_LIMIT),
            FK_facility_to=randint(1, MEDICAL_FACILITIES_LIMIT),
            FK_facility_from=randint(1, MEDICAL_FACILITIES_LIMIT)
        )
        session.add(transfer)
    session.commit()


def generate_patients(session):
    for i in range(0, PATIENTS_LIMIT):
        patient = Patients(
            Name=fake.first_name(),
            Surname=fake.last_name()
        )
        session.add(patient)
    session.commit()


def generate_admissions(session):
    for i in range(0, ADMISSIONS_LIMIT):
        admission_date = fake.date_between(START_DATE, END_DATE)
        discharge_date = None
        if fake.pybool():
            discharge_date = fake.date_between(admission_date, END_DATE)
        admission = Admissions(
            Admission_date=admission_date,
            Discharge_date=discharge_date,
            FK_hospital_ward=randint(1, HOSPITAL_WARDS_LIMIT),
            FK_patient=randint(1, PATIENTS_LIMIT))
        session.add(admission)
    session.commit()


def generate_referrals(session):
    possible_doctors = get_users_with_role(session, 4)
    for i in range(0, REFERRALS_LIMIT):
        body_parts = None
        if fake.pybool():
            body_parts = choice(BODY_PARTS)
        referrals = Referrals(
            Referral_date=fake.date_between(START_DATE, END_DATE),
            Body_part=body_parts,
            FK_user=choice(possible_doctors),
            FK_patient=randint(1, PATIENTS_LIMIT)
        )
        session.add(referrals)
    session.commit()


def generate_medical_exams(session):
    for i in range(0, MEDICAL_EXAMS_LIMIT):
        medical_exam = Medical_exams(
            Name=fake.pystr(5, 45),
        )
        session.add(medical_exam)
    session.commit()


def generate_reservations(session):
    for i in range(0, RESERVATIONS_LIMIT):
        reservation = Reservations(
            Start_date=fake.date_between(start_date=START_DATE, end_date='+1y'),
            Start_time=fake.time(),
            FK_patient=randint(1, PATIENTS_LIMIT),
            FK_medical_exam=randint(1, MEDICAL_EXAMS_LIMIT)
        )
        session.add(reservation)
    session.commit()


def generate_exam_offers(session):
    for i in range(0, RESERVATIONS_LIMIT):
        if fake.pybool():
            daily_limit = randint(1, DAILY_LIMIT_LIMIT)
        else:
            daily_limit = None
        exam_offers = Exam_offers(
            FK_medical_facility=randint(1, MEDICAL_FACILITIES_LIMIT),
            FK_medical_exam=randint(1, MEDICAL_EXAMS_LIMIT),
            Daily_limit=daily_limit
        )
        session.add(exam_offers)
    session.commit()


def generate_employments(session):
    possible_doctors = get_users_with_role(session, 4)
    for i in range(0, MEDICAL_EXAMS_LIMIT):
        employment_date = fake.date_between(EMPLOYMENT_DATE, END_DATE)
        dismissal_date = None
        if fake.pybool():
            dismissal_date = fake.date_between(employment_date, END_DATE)
        employment = Employments(
            FK_medical_facility=randint(1, MEDICAL_FACILITIES_LIMIT),
            FK_user=choice(possible_doctors),
            Employment_date=employment_date,
            Dismissal_date=dismissal_date
        )
        session.add(employment)
    session.commit()


def generate_passengers(session):
    for i in range(0, PASSENGERS_LIMIT):
        passenger = Passengers(
            FK_patient=randint(1, PATIENTS_LIMIT),
            FK_transfer=randint(1, TRANSFERS_LIMIT),
            Needs_care=NEEDS_CARE[randint(0, 1)],
            Status=choice(STATUS),
        )
        session.add(passenger)
    session.commit()


def generate_referrals_medical_exams(session):
    for i in range(0, REFERRALS_MEDICAL_EXAMS):
        referrals_medical_exams = Referrals_Medical_exams(
            FK_medical_exam=randint(1, MEDICAL_EXAMS_LIMIT),
            FK_referral=randint(1, REFERRALS_LIMIT),
        )
        session.add(referrals_medical_exams)
    session.commit()


def generate_users_transfers(session):
    possible_medics = get_users_with_role(session, 5)
    facility_from = randint(1, MEDICAL_FACILITIES_LIMIT)
    facility_to = randint(1, MEDICAL_FACILITIES_LIMIT)
    while facility_to == facility_from:
        facility_to = randint(1, MEDICAL_FACILITIES_LIMIT)
    for i in range(0, USERS_TRANSFERS_LIMIT):
        users_transfers = Users_Transfers(
            FK_user=choice(possible_medics),
            FK_transfer=randint(1, TRANSFERS_LIMIT)
        )
        session.add(users_transfers)
    session.commit()


def generate_all_silent(session):
    generate_users(session)
    generate_roles(session)
    generate_locations(session)
    generate_medical_facilities(session)
    generate_hospital_wards(session)
    generate_vehicles(session)
    generate_transfers(session)
    generate_patients(session)
    generate_admissions(session)
    generate_referrals(session)
    generate_medical_exams(session)
    generate_reservations(session)
    generate_exam_offers(session)
    generate_employments(session)
    generate_passengers(session)
    generate_referrals_medical_exams(session)
    generate_users_transfers(session)


def generate_all_verbose(session):
    generate_users(session)
    print("Generating Users finished")
    generate_roles(session)
    print("Generating Roles finished")
    generate_locations(session)
    print("Generating Locations finished")
    generate_medical_facilities(session)
    print("Generating Medical_facilities finished")
    generate_hospital_wards(session)
    print("Generating Hospital_wards finished")
    generate_vehicles(session)
    print("Generating Vehicles finished")
    generate_transfers(session)
    print("Generating Transfers finished")
    generate_patients(session)
    print("Generating Patients finished")
    generate_admissions(session)
    print("Generating Admissions finished")
    generate_referrals(session)
    print("Generating Referrals finished")
    generate_medical_exams(session)
    print("Generating Medical_exams finished")
    generate_reservations(session)
    print("Generating Reservations finished")
    generate_exam_offers(session)
    print("Generating Exam_offers finished")
    generate_employments(session)
    print("Generating Employments finished")
    generate_passengers(session)
    print("Generating Passengers finished")
    generate_referrals_medical_exams(session)
    print("Generating Referrals_Medical_exams finished")
    generate_users_transfers(session)
    print("Generating Users_Transfers finished")
    print()
    print("-------------------------Database generated :)")


def execute_query_1(session):
    result = session.execute(
        'SELECT users.Name, Surname, "Driver" As Rola FROM transfers left JOIN users ON users.Id_user = transfers.FK_user '
        'left JOIN vehicles ON vehicles.Id_vehicle = transfers.FK_vehicle WHERE transfers.Start_date '
        'BETWEEN :userDate1 AND :userDate2 AND vehicles.License_plate = :plate UNION SELECT users.Name, Surname, '
        '"Medic" As Rola FROM medical_transport.users INNER JOIN users_transfers ON users_transfers.FK_user = users.Id_user '
        'INNER JOIN transfers ON transfers.Id_transfer = users_transfers.FK_transfer INNER JOIN vehicles '
        'ON vehicles.Id_vehicle = transfers.FK_vehicle WHERE transfers.Start_date BETWEEN :userDate1 AND :userDate2 '
        'AND vehicles.License_plate = :plate UNION SELECT patients.Name, patients.Surname, "Patient" As Rola '
        'FROM medical_transport.patients INNER JOIN passengers ON passengers.FK_patient = patients.Id_patient '
        'INNER JOIN transfers ON transfers.Id_transfer = passengers.FK_transfer INNER JOIN vehicles '
        'ON vehicles.Id_vehicle = transfers.FK_vehicle WHERE transfers.Start_date BETWEEN :userDate1 AND :userDate2 '
        'AND vehicles.License_plate = :plate',
        {"userDate1": "2021-08-09", "userDate2": "2022-01-01", "plate": "8EE G59"})

    print('\nQuery 1:')
    for r in result:
        print(r)


def execute_query_2(session):
    result = session.execute(
        'SELECT medical_facilities.Name FROM medical_transport.medical_facilities INNER JOIN locations ON '
        'locations.Id_location = medical_facilities.FK_location INNER JOIN exam_offers ON '
        'exam_offers.FK_medical_facility = medical_facilities.Id_medical_facility INNER JOIN medical_exams ON '
        'medical_exams.Id_medical_exam = exam_offers.FK_medical_exam WHERE medical_exams.Name = :exam_name AND locations.City = :city'
        , {"exam_name": "OsaZyqqKWgizkHvNxMIqMpFdnQi", "city": "Eatonton"})

    print('\nQuery 2: ')
    for r in result:
        print(r)


def execute_query_3(session):
    result = session.execute(
        'SELECT medical_facilities.Name, hospital_wards.name, hospital_wards.places, hospital_wards.places - COUNT(admissions.Id_admission) AS free_places '
        'FROM admissions INNER JOIN hospital_wards ON hospital_wards.Id_hospital_ward = admissions.FK_hospital_ward '
        'INNER JOIN medical_facilities ON medical_facilities.Id_medical_facility = hospital_wards.FK_medical_facility '
        'INNER JOIN locations ON locations.Id_location = medical_facilities.FK_location '
        'WHERE isnull(admissions.Discharge_date) AND locations.city = :city GROUP BY hospital_wards.Id_hospital_ward'
        , {"city": "Gaymouth"})

    print('\nQuery 3')
    for r in result:
        print(r)


def execute_query_4(session):
    result = session.execute(
        'SELECT COUNT(referrals.Id_referral) FROM referrals INNER JOIN refferals_medical_exams '
        'ON refferals_medical_exams.FK_referral = referrals.Id_referral INNER JOIN medical_exams '
        'ON medical_exams.Id_medical_exam = refferals_medical_exams.FK_medical_exam '
        'WHERE medical_exams.Name = :exam_name AND referrals.Referral_date BETWEEN :date_start AND :date_end'
        , {"exam_name": "lSPPZuuXNxvfVGqVfdUVqrkGPdqUqsKc", "date_start": "2021-08-01", "date_end": "2022-01-01"})

    print('\nQuery 4')
    for r in result:
        print(r)


def execute_query_5(session):
    result = session.execute(
        'SELECT patients.name, patients.surname, COUNT(*) AS transports FROM patients LEFT JOIN passengers '
        'ON passengers.FK_patient = patients.Id_patient GROUP BY patients.Id_patient ORDER BY transports DESC LIMIT 10')

    print('\nQuery 5')
    for r in result:
        print(r)


def execute_query_6(session):
    result = session.execute(
        'SELECT users.Name, users.Surname, employments.Employment_date, floor(datediff(now(), employments.Employment_date)/365) '
        'AS seniority FROM users INNER JOIN employments ON employments.FK_user = users.Id_user '
        'INNER JOIN medical_facilities ON medical_facilities.Id_medical_facility = employments.FK_medical_facility '
        'WHERE Dismissal_date IS NULL AND medical_facilities.Name = :name ORDER BY seniority DESC'
        , {"name": "ZoonhFzqgYRmeqJHmxjY"})

    print('\nQuery 6')
    for r in result:
        print(r)


def execute_query_7(session):
    result = session.execute(
        'SELECT AVG(transfers_number) AS Average_Transfers_For_Driver FROM (SELECT users.Name, users.Surname, COUNT(*) '
        'AS transfers_number FROM users INNER JOIN roles ON roles.FK_user = users.Id_user INNER JOIN transfers '
        'ON transfers.FK_user = users.Id_user GROUP BY users.Id_user ORDER BY transfers_number DESC) AS T')

    print('\nQuery 7')
    for r in result:
        print(r)


def execute_query_8(session):
    result = session.execute(
        'SELECT medical_facilities.Name, COUNT(transfers.Id_transfer) AS Transfers from medical_facilities '
        'INNER JOIN transfers ON transfers.FK_facility_to = medical_facilities.Id_medical_facility '
        'GROUP BY medical_facilities.Id_medical_facility ORDER BY Transfers DESC LIMIT 10')

    print('\nQuery 8')
    for r in result:
        print(r)


def execute_query_9(session):
    result = session.execute(
        'SELECT medical_exams.Name as Exam, MAX(exam_offers.Daily_limit) AS "Max Limit", medical_facilities.Name AS Facility '
        'FROM exam_offers LEFT JOIN medical_exams ON medical_exams.Id_medical_exam = exam_offers.FK_medical_exam '
        'LEFT JOIN medical_facilities ON medical_facilities.Id_medical_facility = exam_offers.FK_medical_facility '
        'GROUP BY medical_exams.Name LIMIT 10')

    print('\nQuery 9')
    for r in result:
        print(r)


def execute_query_10(session):
    result = session.execute(
        'SELECT DISTINCT hospital_wards.Name FROM hospital_wards LEFT JOIN medical_facilities '
        'ON medical_facilities.Id_medical_facility = hospital_wards.FK_medical_facility LEFT JOIN locations '
        'ON locations.Id_location = medical_facilities.FK_location WHERE locations.City = :city'
        , {"city": "East Robertomouth"})

    print('\nQuery 10')
    for r in result:
        print(r)

def execute_queries():
    execute_query_1(current_session)
    execute_query_2(current_session)
    execute_query_3(current_session)
    execute_query_4(current_session)
    execute_query_5(current_session)
    execute_query_6(current_session)
    execute_query_7(current_session)
    execute_query_8(current_session)
    execute_query_9(current_session)
    execute_query_10(current_session)


if __name__ == '__main__':
    Session = sessionmaker(bind=mysql_engine, autoflush=False)
    current_session = Session()
    # generate_all_verbose(current_session)
    # generate_all_silent(current_session)
    execute_queries()
    current_session.close()
