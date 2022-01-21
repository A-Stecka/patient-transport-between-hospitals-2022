import datetime

START_DATE = datetime.date(2021, 1, 1)
END_DATE = datetime.date(2021, 11, 1)
EMPLOYMENT_DATE = datetime.date(1950, 1, 1)

SEATS = [1, 4, 5, 6, 7, 8, 9, 10, 13, 17, 18, 19, 20, 24]

ROLES = ["Adm", "Sup", "AEm", "Dri", "Doc", "Med"]

NEEDS_CARE = ["Yes", "No"]

STATUS = ["Lying", "Sitting", "Walking"]

TRANSFER_STATUS = ["Scheduled", "Realised", "Cancelled"]

BODY_PARTS = ["head", "spine", "arm", "hand", "finger", "leg", "knee", "foot", "toe", "stomach", "shoulder", "eye",
              "ear", "breast", "prostate", "heart", "lung", "hip", "pelvis", "appendix", "bladder", "liver", "kidney",
              "chest"]

HOSPITAL_WARDS = ["Oddzial Anestezjologii i Intensywnej Terapii", "Oddzial Chirurgii Ogolnej", "Oddzial Dzieciecy",
                  "Oddzial Chirurgii Ogolnej i Onkologicznej", "Oddzial Chirurgii Urazowo – Ortopedycznej",
                  "Oddzial Chorob Pluc", "Oddzial Chemioterapii", "Oddzial Chorob Wewnetrznych", "Blok operacyjny",
                  "Oddzial Kardiologiczny", "Oddzial Nefrologiczny", "Oddzial Chorob Wewnetrznych",
                  "Oddzial Neonatologiczny", "Oddzial Neurologiczny", "Oddzial Pediatryczny", "Oddzial Nefrologii",
                  "Oddzial Polozniczo – Ginekologiczny", "Oddzial Psychiatryczny", "Oddzial Endokrynologii",
                  "Oddzial Rehabilitacji Neurologicznej", "Oddzial Rehabilitacji Kardiologicznej",
                  "Oddzial Rehabilitacyjny Ogolny", "Oddzial Udarowy", "Oddzial Urologiczny", "Stacja Dializ",
                  "Szpitalny Oddzial Ratunkowy", "Oddzial Kardiochirurgii", "Oddzial Obserwacyjno – Zakazny",
                  "Oddzial Dzienny Psychiatryczny", "Oddzial Chirurgii Plastycznej", "Oddzial Neurochirurgiczny",
                  "Oddzial Okulistyczny", "Oddzial Psychiatryczny", "Oddzial Leczenia Uzaleznien",
                  "Oddzial Rehabilitacyjny", "Oddzial Chirurgii Naczyniowej", "Oddzial Nadcisnienia Tetniczego",
                  "Oddzial Gastroenterologii", "Oddzial Laryngologiczny", "Oddzial Onkologii Klinicznej",
                  "Oddzial Reumatologiczny", "Oddzial Otolaryngologiczny", "Oddzial Geriatryczny"]

# users limits
ADM_EMPLOYEE_LIMIT = 500
DOCTORS_LIMIT = 2000
MEDICS_LIMIT = 1000
DRIVERS_LIMIT = 750
SUPERVISORS_LIMIT = 100
ADMINISTRATORS_LIMIT = 100

# other limits
LOCATIONS_LIMIT = 1250
MEDICAL_FACILITIES_LIMIT = 400
HOSPITAL_WARDS_LIMIT = 1500
VEHICLES_LIMIT = 1000
TRANSFERS_LIMIT = 7000
PATIENTS_LIMIT = 7500
REFERRALS_LIMIT = 9000
MEDICAL_EXAMS_LIMIT = 175

# relationships limits <3
MEDICS_IN_TRANSFER_LIMIT = 4
OFFERS_LIMIT = 3000
WARDS_IN_FACILITY_LIMIT = 10
MEDICAL_FACILITY_HAS_LIMIT = 10
PARTICIPATES_LIMIT = 5
GETS_LIMIT = 20
IS_OCCUPIED_LIMIT = 10000

DAILY_LIMIT_LIMIT = 75
PLACES_IN_WARD_LIMIT = 80
POSTAL_CODE_LOWER_LIMIT = 10000
POSTAL_CODE_UPPER_LIMIT = 99999
