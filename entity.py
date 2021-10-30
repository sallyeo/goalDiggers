import db_helper


# id | user_type_id | name | email | address | phone_number | user_type | password #
class User:
    DATABASE = db_helper.db_helper()

    def __init__(self, id, user_type_id, name, email, address, phone_number, user_type):
        self.id = id
        self.user_type_id = user_type_id
        self.name = name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.user_type = user_type

    def __str__(self):
        return f'User: {{\n' \
               f'\t\'id\': {self.id},\n' \
               f'\t\'user_type_id\': \'{self.user_type_id}\',\n' \
               f'\t\'name\': \'{self.name}\',\n' \
               f'\t\'email\': \'{self.email}\',\n' \
               f'\t\'address\': \'{self.address}\',\n' \
               f'\t\'phone_number\': \'{self.phone_number}\',\n' \
               f'\t\'user_type\': \'{self.user_type}\',\n' \
               f'}},'


# date | string_code | prescription_id | patient_id | doctor_id | status | prescription_detail #
class Prescription:
    DATABASE = db_helper.db_helper()

    def __init__(self, date, code, prescription_id, patient_id, doctor_id, status, prescription_detail):
        self.date = date
        self.code = code
        self.prescription_id = prescription_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.status = status
        self.prescription_detail = prescription_detail

    def __str__(self):
        return f'Prescription: {{\n' \
               f'\t\'date\': {self.date},\n' \
               f'\t\'code\': \'{self.code}\',\n' \
               f'\t\'prescription_id\': \'{self.prescription_id}\',\n' \
               f'\t\'patient_id\': \'{self.patient_id}\',\n' \
               f'\t\'doctor_id\': \'{self.doctor_id}\',\n' \
               f'\t\'status\': \'{self.status}\',\n' \
               f'\t\'prescription_detail\': \'{self.prescription_detail}\',\n' \
               f'}},'


# id | medicine_name #
class Medicine:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f'Medicine: {{\n' \
               f'\t\'id\': {self.id},\n' \
               f'\t\'name\': \'{self.name}\',\n' \
               f'}},'


class ObjectEntity:
    DATABASE = db_helper.db_helper()

    def retrieve_one(self, query):
        # result = self.retrieve_all(query)
        result = ObjectEntity.DATABASE.query_db(query)
        if len(result) > 0:
            return result[0]
        return []

    def retrieve_all(self, query):
        return ObjectEntity.DATABASE.query_db(query)


class UserEntity(ObjectEntity):
    def retrieve_one(self, object_id):
        query = f"SELECT * FROM USERS WHERE user_type_id = '{object_id}'"
        result = super(UserEntity, self).retrieve_one(query)
        # print(f'result: {result}')
        if len(result) > 0:
            return User(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
        return result
        # results = ObjectEntity.DATABASE.query_db(query)
        # if len(results) > 0:
        #     r = results[0]
        #     user = User(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
        #     return user
        # return False

    def retrieve_all(self, query=None):
        query = f"SELECT * FROM USERS"
        result = super(UserEntity, self).retrieve_all(query)
        users = []
        for r in result:
            user = User(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
            users.append(user)
        return users
        # result = ObjectEntity.DATABASE.query_db(query)

    def validate_login(self, email, password):
        validation_query = f"SELECT * FROM USERS WHERE email = '{email}' AND PASSWORD = '{password}'"
        result = ObjectEntity.DATABASE.query_db(validation_query)
        if len(result) > 0:
            r = result[0]
            return User(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
        return result
        # return self.retrieve_one(validation_query)


class PrescriptionEntity(ObjectEntity):
    def retrieve_one(self, object_id):
        query = f"SELECT * FROM PRESCRIPTION WHERE string_code = '{object_id}'"
        result = super(PrescriptionEntity, self).retrieve_one(query)
        if len(result) > 0:
            return Prescription(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
        return result

    def retrieve_all(self, query=None):
        if query is None:
            query = f"SELECT * FROM PRESCRIPTION"
        result = super(PrescriptionEntity, self).retrieve_all(query)
        prescriptions = []
        for r in result:
            prescription = Prescription(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
            prescriptions.append(prescription)
        return prescriptions

    def retrieve_by_fk(self, fk):
        query = f"SELECT * FROM PRESCRIPTION WHERE patient_id = '{fk}'"
        print(f'query: {fk}')
        return self.retrieve_all(query)


class MedicineEntity(ObjectEntity):
    def retrieve_one(self, object_id):
        query = f"SELECT * FROM MEDICINE WHERE id = '{object_id}'"
        return super(MedicineEntity, self).retrieve_one(query)
        # if len(result) > 0:
        #     return Medicine(result[0], result[1])
        # return result

    def retrieve_all(self, query=None):
        query = f"SELECT * FROM MEDICINE"
        # result = ObjectEntity.DATABASE.query_db(query)
        result = super(MedicineEntity, self).retrieve_all(query)
        medicines = []
        for r in result:
            medicine = Medicine(r[0], r[1])
            medicines.append(medicine)
        return medicines

    # def retrieve_by_fk(self, fk):
    #     query = f"-- SELECT * FROM MEDICINE WHERE prescription_id"
