import db_helper
from dataclasses import dataclass, field
from hashlib import sha256


DATABASE = db_helper.db_helper()


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

    def __hash__(self):
        return hash(self.object_id)

    def __eq__(self, other):
        return self.object_id == other.object_id

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

    def __eq__(self, other):
        return self.object_id == other.object_id


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
        final = ' OR '.join(conditions)
        query = f'SELECT * FROM {table} WHERE {final}'
        print(f'search {query}')
        result = DATABASE.query_db(query)
        return result


class UserTypeEntity(ObjectEntity):
    def retrieve_by_id(self, role):
        return self.get_one(self.retrieve_by_conditions('UserType', role=role))

    def retrieve_all(self):
        return self.get_many(super(UserTypeEntity, self).retrieve_by_conditions('UserType'))

    def get_one(self, result):
        if len(result) > 0:
            r = result[0]
            return UserType(r[0])

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

    # def hash_all_passwords(self):
    #     all_users = self.retrieve_by_conditions('User')
    #     for user in all_users:
    #         object_id = user[0]
    #         encrypted = sha256(user[6].encode('ascii')).hexdigest()
    #         print(f'{object_id = }, {encrypted}')
    #         self.save('User', object_id, password=encrypted)


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
        if len(result) > 0:
            r = result[0]
            return MedicineQuantity(r[0], r[1], r[2], r[3], r[4])

    def get_many(self, result):
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
