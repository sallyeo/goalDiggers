import db_helper


# id | role #
class UserType:
    def __init__(self, object_id, role):
        self.object_id = object_id
        self.role = role

    def __str__(self):
        return f'UserType: {{\n' \
               f'\t\'id\': {self.object_id},\n' \
               f'\t\'role\': \'{self.role}\',\n' \
               f'}},'


# id | email | name | phone_number | address | role | password #
class User:
    def __init__(self, object_id, email, name, phone_number, address, role, password):
        self.object_id = object_id
        self.email = email
        self.name = name
        self.phone_number = phone_number
        self.address = address
        self.role = role
        self.password = password

    def __str__(self):
        return f'User: {{\n' \
               f'\t\'id\': {self.object_id},\n' \
               f'\t\'email\': \'{self.email}\',\n' \
               f'\t\'name\': \'{self.name}\',\n' \
               f'\t\'phone_number\': \'{self.phone_number}\',\n' \
               f'\t\'address\': \'{self.address}\',\n' \
               f'\t\'role\': \'{self.role}\',\n' \
               f'\t\'password\': \'{self.password}\',\n' \
               f'}},'


# id | name #
class Medicine:
    def __init__(self, object_id, name):
        self.object_id = object_id
        self.name = name

    def __str__(self):
        return f'Medicine: {{\n' \
               f'\t\'id\': {self.object_id},\n' \
               f'\t\'name\': \'{self.name}\',\n' \
               f'}},'


# id | patient_id #
class Cart:
    def __init__(self, object_id, patient_id):
        self.object_id = object_id
        self.patient_id = patient_id

    def __str__(self):
        return f'Cart: {{\n' \
               f'\t\'object_id\': {self.object_id},\n' \
               f'\t\'patient_id\': {self.patient_id},\n' \
               f'}},'


# id | date_created | doctor_id | patient_id | pharmacist_id | collected #
class Prescription:
    def __init__(self, object_id, date_created, doctor_id, patient_id, pharmacist_id, collected):
        self.object_id = object_id
        self.date_created = date_created
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.pharmacist_id = pharmacist_id
        self.collected = collected

    def get_status_string(self):
        return 'Collected' if self.collected == 1 else 'Not Collected'

    def __str__(self):
        return f'Prescription: {{\n' \
               f'\t\'id\': {self.object_id},\n' \
               f'\t\'date_created\': {self.date_created},\n' \
               f'\t\'doctor_id\': {self.doctor_id},\n' \
               f'\t\'patient_id\': {self.patient_id},\n' \
               f'\t\'pharmacist_id\': {self.pharmacist_id},\n' \
               f'\t\'collected\': {self.collected},\n' \
               f'}},'


# id | prescription_id | cart_id | medicine_id | quantity #
class MedicineQuantity:
    def __init__(self, object_id, prescription_id, cart_id, medicine_id, quantity):
        self.object_id = object_id
        self.prescription_id = prescription_id
        self.cart_id = cart_id
        self.medicine_id = medicine_id
        self.quantity = quantity

    def __str__(self):
        return f'MedicineQuantity: {{\n' \
               f'\t\'id\': {self.object_id},\n' \
               f'\t\'prescription_id\': \'{self.prescription_id}\',\n' \
               f'\t\'cart_id\': \'{self.cart_id}\',\n' \
               f'\t\'medicine_id\': \'{self.medicine_id}\',\n' \
               f'\t\'quantity\': \'{self.quantity}\',\n' \
               f'}},'


class ObjectEntity:
    DATABASE = db_helper.db_helper()

    @staticmethod
    def retrieve_by_conditions(table, **kwargs):
        joined = ''
        # Join conditions
        if len(kwargs) > 0:
            conditions = []
            for key, value in kwargs.items():
                conditions.append(f"{key} = '{value}'")
            print(f'{conditions = }')
            joined = ' WHERE ' + ' AND '.join(conditions)

        query = f"SELECT * FROM {table}{joined}"
        print(f'{query = }')
        result = ObjectEntity.DATABASE.query_db(query)
        print(f'{result = }')
        return result

    def retrieve_by_id(self, value):
        pass

    def get_one_or_none(self, object_id):
        pass

    def get_many_or_none(self, result):
        pass


class UserTypeEntity(ObjectEntity):
    def retrieve_by_id(self, role):
        return self.get_one_or_none(self.retrieve_by_conditions('UserType', role=role))

    def retrieve_all(self):
        return self.get_many_or_none(super(UserTypeEntity, self).retrieve_by_conditions('UserType'))

    def get_one_or_none(self, result):
        if len(result) > 0:
            r = result[0]
            return UserType(r[0], r[1])
        return None

    def get_many_or_none(self, result):
        user_types = []
        for r in result:
            user_type = UserType(r[0], r[1])
            user_types.append(user_type)
        return user_types


class UserEntity(ObjectEntity):
    def retrieve_by_id(self, object_id):
        return self.get_one_or_none(super(UserEntity, self).retrieve_by_conditions('User', id=object_id))

    def retrieve_by_email(self, email):
        return self.get_one_or_none(super(UserEntity, self).retrieve_by_conditions('User', email=email))

    def retrieve_by_phone_number(self, phone_number):
        return self.get_one_or_none(super(UserEntity, self).retrieve_by_conditions('User', phone_number=phone_number))

    def retrieve_all(self):
        return self.get_many_or_none(super(UserEntity, self).retrieve_by_conditions('User'))

    def get_one_or_none(self, result):
        if len(result) > 0:
            r = result[0]
            return User(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
        return None

    def get_many_or_none(self, result):
        users = []
        for r in result:
            user = User(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
            users.append(user)
        return users

    def validate_login(self, email, password):
        result = super(UserEntity, self).retrieve_by_conditions('User', email=email, password=password)
        if len(result) > 0:
            r = result[0]
            return User(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
        return result

    def save(self, user):
        print(f'saving {user = }')


class PrescriptionEntity(ObjectEntity):
    def retrieve_by_id(self, object_id):
        return self.get_one_or_none(super(PrescriptionEntity, self).retrieve_by_conditions('Prescription', id=object_id))

    def retrieve_all(self):
        return self.get_many_or_none(super(PrescriptionEntity, self).retrieve_by_conditions('Prescription'))

    def retrieve_by_patient(self, patient_id):
        return self.get_many_or_none(super(PrescriptionEntity, self).retrieve_by_conditions('Prescription', patient_id=patient_id))

    def get_one_or_none(self, result):
        if len(result) > 0:
            r = result[0]
            return Prescription(r[0], r[1], r[2], r[3], r[4], r[5])
        return None

    def get_many_or_none(self, result):
        prescriptions = []
        for r in result:
            prescription = Prescription(r[0], r[1], r[2], r[3], r[4], r[5])
            prescriptions.append(prescription)
        return prescriptions


class MedicineEntity(ObjectEntity):
    def retrieve_by_id(self, object_id):
        return self.get_one_or_none(super(MedicineEntity, self).retrieve_by_conditions('Medicine', id=object_id))

    def retrieve_all(self):
        return self.get_many_or_none(super(MedicineEntity, self).retrieve_by_conditions('Medicine'))

    def get_one_or_none(self, result):
        if len(result) > 0:
            r = result[0]
            return Medicine(r[0], r[1])
        return None

    def get_many_or_none(self, result):
        medicines = []
        for r in result:
            medicine = Medicine(r[0], r[1])
            medicines.append(medicine)
        return medicines


class MedicineQuantityEntity(ObjectEntity):
    def retrieve_by_id(self, object_id):
        return self.get_one_or_none(super(MedicineQuantityEntity, self).retrieve_by_conditions('MedicineQuantity', id=object_id))

    def retrieve_all(self):
        return self.get_many_or_none(super(MedicineQuantityEntity, self).retrieve_by_conditions('MedicineQuantity'))

    def retrieve_by_prescription(self, prescription_id):
        return self.get_many_or_none(super(MedicineQuantityEntity, self).retrieve_by_conditions('MedicineQuantity', prescription_id=prescription_id))

    def retrieve_by_cart(self, cart_id):
        return self.get_many_or_none(super(MedicineQuantityEntity, self).retrieve_by_conditions('MedicineQuantity', cart_id=cart_id))

    def get_one_or_none(self, result):
        if not result:
            return None
        if len(result) > 0:
            r = result[0]
            return MedicineQuantity(r[0], r[1], r[2], r[3], r[4])

    def get_many_or_none(self, result):
        if not result:
            return None
        medicine_quantities = []
        for r in result:
            medicine_quantity = MedicineQuantity(r[0], r[1], r[2], r[3], r[4])
            medicine_quantities.append(medicine_quantity)
            return medicine_quantities
