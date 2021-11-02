from sqlite3 import IntegrityError

import entity as E


class Session:
    user = None
    context = {}

    @staticmethod
    def set_user(user):
        Session.user = user

    @staticmethod
    def get_user():
        return Session.user

    @staticmethod
    def set_context(key, value):
        Session.context[key] = value

    @staticmethod
    def get_context(key):
        return Session.context[key]


class UserTypeController:
    @staticmethod
    def retrieve_all_roles():
        return E.UserTypeEntity().retrieve_all()
    
    @staticmethod
    def retrieve_role(role):
        return E.UserTypeEntity().retrieve_by_id(role)


# REMINDER FOR DESMOND: PASS IN QUERYING USER OBJECT TO CHECK VALIDITY
class UserController:
    @staticmethod
    def retrieve_all_users():
        return E.UserEntity().retrieve_all()
        
    @staticmethod
    def retrieve_user(user_id):
        return E.UserEntity().retrieve_by_id(user_id)

    @staticmethod
    def retrieve_users_by_role(role):
        role_obj = UserTypeController.retrieve_role(role)
        if not role:
            raise ValueError('No such role')
        return E.UserEntity().retrieve_all_by_role(role_obj.role)

    @staticmethod
    def login(email, password):
        if email == "" or password == "":
            return False
        return E.UserEntity().validate_login(email, password)

    @staticmethod
    def save_user(user_id, email, name, phone_number, address, role):
        user_id = int(user_id)
        if UserController.check_email_match(email, user_id):
            raise IntegrityError(f'Email must be unique.')
        if UserController.check_phone_number_match(phone_number, user_id):
            raise IntegrityError(f'Phone number must be unique')
        E.UserEntity().save(
            'User',
            user_id,
            email=email,
            name=name,
            phone_number=phone_number,
            address=address,
            role=role
        )

    @staticmethod
    def create_user(email, name, phone_number, address, role, password):
        if not email or not name or not phone_number or not address or not role or not password:
            raise ValueError('Please fill in all fields')
        if not UserController.check_email_match(email):
            raise IntegrityError('Email must be unique.')
        if not UserController.check_phone_number_match(phone_number):
            raise IntegrityError('Phone number must be unique')
        E.UserEntity().create('User', email=email, name=name, phone_number=phone_number, address=address, role=role, password=password)

    @staticmethod
    def check_email_match(email, user_id=None):
        email_check = E.UserEntity().retrieve_all_by_email(email)
        # If email_check list has elements and user_id is valid
        if email_check and user_id:
            if len(email_check) > 1 or email_check[0].object_id != user_id:
                return False
        return True

    @staticmethod
    def check_phone_number_match(phone_number, user_id=None):
        phone_number_check = E.UserEntity().retrieve_all_by_email(phone_number)
        # If phone_number_check list has elements and user_id is valid
        if phone_number_check and user_id:
            if len(phone_number_check) > 1 or phone_number_check[0].object_id != user_id:
                return False
        return True


class PrescriptionController:
    e = E.PrescriptionEntity()

    @staticmethod
    def retrieve_all_prescriptions():
        return PrescriptionController.e.retrieve_all()

    @staticmethod
    def retrieve_prescription(code):
        return PrescriptionController.e.retrieve_by_id(code)

    @staticmethod
    def retrieve_patient_prescriptions(patient_id):
        return PrescriptionController.e.retrieve_by_patient(patient_id)


class MedicineController:
    e = E.MedicineEntity()

    @staticmethod
    def retrieve_by_id(medicine_id):
        return MedicineController.e.retrieve_by_id(medicine_id)

    @staticmethod
    def retrieve_by_name(medicine_name):
        return MedicineController.e.retrieve_by_name(medicine_name)

    @staticmethod
    def retrieve_all_medicines():
        return MedicineController.e.retrieve_all()


class MedicineQuantityController:
    e = E.MedicineQuantityEntity()

    @staticmethod
    def retrieve_by_id(object_id):
        return MedicineQuantityController.e.retrieve_by_id(object_id)

    @staticmethod
    def retrieve_prescription_medicines(prescription_id):
        return MedicineQuantityController.e.retrieve_by_prescription(prescription_id)

    @staticmethod
    def retrieve_cart_medicines(cart_id):
        return MedicineQuantityController.e.retrieve_by_cart(cart_id)

    @staticmethod
    def add_new(quantity, medicine_name, patient_id):
        try:
            quantity = int(quantity)
        except ValueError as err:
            print('Quantity must be an integer !')
        medicine_id = MedicineController.retrieve_by_name(medicine_name).object_id
        cart_id = CartController.retrieve_cart_by_patient(patient_id).object_id
        cart_medicines = MedicineQuantityController.e.retrieve_by_cart(cart_id)
        matched = False
        if cart_medicines:
            for medicine_quantity in cart_medicines:
                if medicine_quantity.medicine_id == medicine_id:
                    medicine_quantity.quantity += quantity
                    matched = True
                    MedicineQuantityController.e.save_object(medicine_quantity)
        if not matched:
            MedicineQuantityController.e.create('MedicineQuantity', cart_id=cart_id, medicine_id=medicine_id, quantity=quantity)

    @staticmethod
    def save_medicine_quantity(object_id, prescription_id, cart_id, medicine_id, quantity):
        object_id = int(object_id)
        # if not MedicineQuantityController.check_cart_and_id(cart_id, object_id):
        #     raise ValueError('Cart object_id does not match')
        medicine_quantity = MedicineQuantityController.e.retrieve_by_id(object_id)
        medicine_quantity.prescription_id = prescription_id
        medicine_quantity.cart_id = cart_id
        medicine_quantity.medicine_id = medicine_id
        medicine_quantity.quantity = quantity
        MedicineQuantityController.e.save_object(medicine_quantity)

    # @staticmethod
    # def check_cart_and_id(cart_id, object_id):
    #     cart_check = E.MedicineQuantityEntity().retrieve_by_cart(cart_id)
    #     return cart_check.object_id == object_id

    @staticmethod
    def delete(object_id):
        MedicineQuantityController.e.delete('MedicineQuantity', id=object_id)


class CartController:
    e = E.CartEntity()
    
    @staticmethod
    def retrieve_cart_by_id(object_id):
        return CartController.e.retrieve_by_id(object_id)

    @staticmethod
    def retrieve_cart_by_patient(object_id):
        user = UserController.retrieve_user(object_id)
        if user.role != 'Patient':
            raise ValueError('User is not a patient.')
        cart = CartController.e.retrieve_by_patient(object_id)
        if not cart:
            CartController.e.create('Cart', patient_id=object_id)
            cart = CartController.e.retrieve_by_patient(object_id)
        return cart
    
    @staticmethod
    def create_patient_cart(patient_id):
        return CartController.e.create('Cart', patient_id=patient_id)
    