import db_helper
from dataclasses import dataclass, field


DATABASE = db_helper.db_helper()


# id | role #
# class UserType:
#     def __init__(self, role: str):
#         self._role = role
#
#     @property
#     def role(self):
#         return self._role
#
#     @role.setter
#     def role(self, role: str):
#         self._role = role
#
#     def __repr__(self):
#         return self.role
#
#     def __str__(self):
#         return f'UserType: {{\n' \
#                f'\t\'role\': \'{self.role}\',\n' \
#                f'}},'


# id | email | name | phone_number | address | role | password #
# class User:
#     def __init__(self, object_id: int, email: str, name: str, phone_number: str, address: str, role: str):
#         self._object_id = object_id
#         self._email = email
#         self._name = name
#         self._phone_number = phone_number
#         self._address = address
#         self._role = role
#
#     @property
#     def object_id(self):
#         return self._object_id
#
#     @object_id.setter
#     def object_id(self, object_id: int):
#         try:
#             self._object_id = int(object_id)
#         except ValueError:
#             print('object_id must be an int')
#
#     @property
#     def email(self):
#         return self._email
#
#     @email.setter
#     def email(self, email: str):
#         self._email = email
#
#     @property
#     def name(self):
#         return self._name
#
#     @name.setter
#     def name(self, name: str):
#         self._email = name
#
#     @property
#     def phone_number(self):
#         return self._phone_number
#
#     @phone_number.setter
#     def phone_number(self, phone_number: str):
#         self._phone_number = phone_number
#
#     @property
#     def address(self):
#         return self._address
#
#     @address.setter
#     def address(self, address: str):
#         self._address = address
#
#     @property
#     def role(self):
#         return self._role
#
#     @role.setter
#     def role(self, role: str):
#         self._role = role
#
#     def __repr__(self):
#         return str([self.object_id, self.email, self.name, self.phone_number, self.address])
#
#     def __str__(self):
#         return f'User: {{\n' \
#                f'\t\'id\': {self._object_id},\n' \
#                f'\t\'email\': \'{self._email}\',\n' \
#                f'\t\'name\': \'{self._name}\',\n' \
#                f'\t\'phone_number\': \'{self._phone_number}\',\n' \
#                f'\t\'address\': \'{self._address}\',\n' \
#                f'\t\'role\': \'{self._role}\',\n' \
#                f'}},'


# id | name #
# class Medicine:
#     def __init__(self, object_id: int, name: str):
#         self._object_id = object_id
#         self._name = name
#
#     @property
#     def object_id(self):
#         return self._object_id
#
#     @object_id.setter
#     def object_id(self, object_id: int):
#         try:
#             self._object_id = int(object_id)
#         except ValueError:
#             print('object_id must be an integer !')
#
#     @property
#     def name(self):
#         return self._name
#
#     @name.setter
#     def name(self, name: int):
#         self._name = int(name)
#
#     def __repr__(self):
#         return [self.object_id, self.name]
#
#     def __str__(self):
#         return f'Medicine: {{\n' \
#                f'\t\'id\': {self._object_id},\n' \
#                f'\t\'name\': \'{self._name}\',\n' \
#                f'}},'


# id | patient_id #
# class Cart:
#     def __init__(self, object_id, patient_id):
#         self.object_id = object_id
#         self.patient_id = patient_id
#
#     def __str__(self):
#         return f'Cart: {{\n' \
#                f'\t\'object_id\': {self.object_id},\n' \
#                f'\t\'patient_id\': {self.patient_id},\n' \
#                f'}},'


# id | date_created | doctor_id | patient_id | pharmacist_id | collected #
# class Prescription:
#     def __init__(self, object_id, date_created, doctor_id, patient_id, pharmacist_id, collected):
#         self.object_id = object_id
#         self.date_created = date_created
#         self.doctor_id = doctor_id
#         self.patient_id = patient_id
#         self.pharmacist_id = pharmacist_id
#         self.collected = collected
#
#     def get_status_string(self):
#         return 'Collected' if self.collected == 1 else 'Not Collected'
#
#     def __str__(self):
#         return f'Prescription: {{\n' \
#                f'\t\'id\': {self.object_id},\n' \
#                f'\t\'date_created\': {self.date_created},\n' \
#                f'\t\'doctor_id\': {self.doctor_id},\n' \
#                f'\t\'patient_id\': {self.patient_id},\n' \
#                f'\t\'pharmacist_id\': {self.pharmacist_id},\n' \
#                f'\t\'collected\': {self.collected},\n' \
#                f'}},'


# id | prescription_id | cart_id | medicine_id | quantity #
# class MedicineQuantity:
#     def __init__(self, object_id, prescription_id, cart_id, medicine_id, quantity):
#         self.object_id = object_id
#         self.prescription_id = prescription_id
#         self.cart_id = cart_id
#         self.medicine_id = medicine_id
#         self.quantity = quantity
#
#     def __str__(self):
#         return f'MedicineQuantity: {{\n' \
#                f'\t\'id\': {self.object_id},\n' \
#                f'\t\'prescription_id\': \'{self.prescription_id}\',\n' \
#                f'\t\'cart_id\': \'{self.cart_id}\',\n' \
#                f'\t\'medicine_id\': \'{self.medicine_id}\',\n' \
#                f'\t\'quantity\': \'{self.quantity}\',\n' \
#                f'}},'


# id | role #
@dataclass
class UserType:
    role: str


# id | email | name | phone_number | address | role | password #
@dataclass
class User:
    object_id: int
    email: str
    name: str
    phone_number: str
    address: str
    role: str


# id | name #
@dataclass
class Medicine:
    object_id: int
    name: str


# id | patient_id #
@dataclass
class Cart:
    object_id: int
    patient_id: int


# id | date_created | doctor_id | patient_id | pharmacist_id | collected #
@dataclass
class Prescription:
    object_id: int
    date_created: str
    doctor_id: int
    patient_id: int
    pharmacist_id: int
    collected: int

    def get_status_string(self):
        return 'Collected' if self.collected == 1 else 'Not Collected'


# id | prescription_id | cart_id | medicine_id | quantity #
@dataclass
class MedicineQuantity:
    object_id: int
    prescription_id: int
    cart_id: int
    medicine_id: int
    quantity: int


class ObjectEntity:
    @staticmethod
    def retrieve_by_conditions(table, **kwargs):
        joined = ''
        # Join conditions
        if len(kwargs) > 0:
            conditions = []
            for key, value in kwargs.items():
                conditions.append(f"{key} = '{value}'")
            joined = ' WHERE ' + ' AND '.join(conditions)

        query = f"SELECT * FROM {table}{joined}"
        result = DATABASE.query_db(query)
        return result

    def retrieve_by_id(self, value):
        pass

    def get_one(self, object_id):
        pass

    def get_many(self, result):
        pass

    @staticmethod
    def save(table, object_id, **kwargs):
        columns = []
        for key, value in kwargs.items():
            print(f'{value = }')
            if value == 'None':
                value = 'NULL'
            columns.append(f"{key} = '{value}'")
        joined = ', '.join(columns)
        query = f"UPDATE {table} SET {joined} WHERE id = {object_id}"
        print(f'save {query =}')
        result = DATABASE.query_db(query)
        print(f'{result = }')
        return result

    @staticmethod
    def create(table, **kwargs):
        columns = ','.join(kwargs.keys())
        data = ','.join(f"'{word}'" for word in kwargs.values())
        query = f'INSERT INTO {table} ({columns}) VALUES ({data})'
        print(f'create {query = }')
        row_id = DATABASE.create(query)
        return row_id

    @staticmethod
    def delete(table, **kwargs):
        conditions = []
        for key, value in kwargs.items():
            condition = [key, f"'{value}'"]
            joined = '='.join(condition)
            conditions.append(joined)
        final = ' AND '.join(conditions)
        query = f'DELETE FROM {table} WHERE {final}'
        print(f'delete {query = }')
        result = DATABASE.query_db(query)
        return result

    @staticmethod
    def search(table, **kwargs):
        conditions = []
        for key, value in kwargs.items():
            condition = [key, f"'%{value}%'"]
            joined = ' LIKE '.join(condition)
            conditions.append(joined)
        final = ' OR '.join[conditions]
        query = f'SELECT * FROM {table} WHERE {final}'
        print(f'{query}')


class UserTypeEntity(ObjectEntity):
    def retrieve_by_id(self, role):
        return self.get_one(self.retrieve_by_conditions('UserType', role=role))

    def retrieve_all(self):
        return self.get_many(super(UserTypeEntity, self).retrieve_by_conditions('UserType'))

    def get_one(self, result):
        if len(result) > 0:
            r = result[0]
            return UserType(r[0])
        return None

    def get_many(self, result):
        user_types = []
        for r in result:
            user_type = UserType(r[0])
            user_types.append(user_type)
        return user_types


class UserEntity(ObjectEntity):
    def retrieve_by_id(self, object_id):
        return self.get_one(super(UserEntity, self).retrieve_by_conditions('User', id=object_id))

    def retrieve_by_email(self, email):
        return self.get_one(super(UserEntity, self).retrieve_by_conditions('User', email=email))

    def retrieve_by_phone_number(self, phone_number):
        return self.get_one(super(UserEntity, self).retrieve_by_conditions('User', phone_number=phone_number))

    def retrieve_all_by_role(self, role):
        return self.get_many(super(UserEntity, self).retrieve_by_conditions('User', role=role))

    def retrieve_all(self):
        return self.get_many(super(UserEntity, self).retrieve_by_conditions('User'))

    def get_one(self, result):
        if len(result) > 0:
            r = result[0]
            return User(r[0], r[1], r[2], r[3], r[4], r[5])
        return None

    def get_many(self, result):
        users = []
        for r in result:
            user = User(r[0], r[1], r[2], r[3], r[4], r[5])
            users.append(user)
        return users

    def validate_login(self, email, password):
        result = super(UserEntity, self).retrieve_by_conditions('User', email=email, password=password)
        if len(result) > 0:
            r = result[0]
            return User(r[0], r[1], r[2], r[3], r[4], r[5])
        return result


class CartEntity(ObjectEntity):
    def retrieve_by_id(self, object_id):
        return self.get_one(super(CartEntity, self).retrieve_by_conditions('Cart', id=object_id))

    def retrieve_by_patient(self, patient_id):
        return self.get_one(super(CartEntity, self).retrieve_by_conditions('Cart', patient_id=patient_id))

    def retrieve_all(self):
        return self.get_many(super(CartEntity, self).retrieve_by_conditions('Cart'))

    def get_one(self, result):
        if len(result) > 0:
            r = result[0]
            return Cart(r[0], r[1])
        return None

    def get_many(self, result):
        users = []
        for r in result:
            user = Cart(r[0], r[1])
            users.append(user)
        return users


class PrescriptionEntity(ObjectEntity):
    def retrieve_by_id(self, object_id):
        return self.get_one(super(PrescriptionEntity, self).retrieve_by_conditions('Prescription', id=object_id))

    def retrieve_all(self):
        return self.get_many(super(PrescriptionEntity, self).retrieve_by_conditions('Prescription'))

    def retrieve_by_patient(self, patient_id):
        return self.get_many(super(PrescriptionEntity, self).retrieve_by_conditions('Prescription', patient_id=patient_id))

    def get_one(self, result):
        if len(result) > 0:
            r = result[0]
            return Prescription(r[0], r[1], r[2], r[3], r[4], r[5])
        return None

    def get_many(self, result):
        prescriptions = []
        for r in result:
            prescription = Prescription(r[0], r[1], r[2], r[3], r[4], r[5])
            prescriptions.append(prescription)
        return prescriptions


class MedicineEntity(ObjectEntity):
    def retrieve_by_id(self, object_id):
        return self.get_one(super(MedicineEntity, self).retrieve_by_conditions('Medicine', id=object_id))

    def retrieve_by_name(self, name):
        return self.get_one(super(MedicineEntity, self).retrieve_by_conditions('Medicine', name=name))

    def retrieve_all(self):
        return self.get_many(super(MedicineEntity, self).retrieve_by_conditions('Medicine'))

    def get_one(self, result):
        if len(result) > 0:
            r = result[0]
            return Medicine(r[0], r[1])
        return None

    def get_many(self, result):
        medicines = []
        for r in result:
            medicine = Medicine(r[0], r[1])
            medicines.append(medicine)
        return medicines


class MedicineQuantityEntity(ObjectEntity):
    table_name = 'MedicineQuantity'

    def retrieve_by_id(self, object_id):
        return self.get_one(super(MedicineQuantityEntity, self).retrieve_by_conditions(self.table_name, id=object_id))

    def retrieve_all(self):
        return self.get_many(super(MedicineQuantityEntity, self).retrieve_by_conditions(self.table_name))

    def retrieve_by_prescription(self, prescription_id):
        return self.get_many(super(MedicineQuantityEntity, self).retrieve_by_conditions(self.table_name, prescription_id=prescription_id))

    def retrieve_by_cart(self, cart_id):
        medicines = self.get_many(super(MedicineQuantityEntity, self).retrieve_by_conditions(self.table_name, cart_id=cart_id))
        print(f'{medicines = }')
        return medicines

    def get_one(self, result):
        if not result:
            return None
        if len(result) > 0:
            r = result[0]
            return MedicineQuantity(r[0], r[1], r[2], r[3], r[4])

    def get_many(self, result):
        if not result:
            return None
        medicine_quantities = []
        for r in result:
            medicine_quantity = MedicineQuantity(r[0], r[1], r[2], r[3], r[4])
            medicine_quantities.append(medicine_quantity)
        return medicine_quantities

    def save_object(self, medicine_quantity):
        self.save(
            self.table_name,
            medicine_quantity.object_id,
            prescription_id=medicine_quantity.prescription_id,
            cart_id=medicine_quantity.cart_id,
            medicine_id=medicine_quantity.medicine_id,
            quantity=medicine_quantity.quantity,
        )
