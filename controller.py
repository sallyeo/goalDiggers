from sqlite3 import IntegrityError

import entity as E


class Session:
    user = None
    context = None

    @staticmethod
    def set_user(user):
        Session.user = user

    @staticmethod
    def get_user():
        return Session.user

    @staticmethod
    def set_context(context):
        Session.context = context

    @staticmethod
    def get_context():
        return Session.context


# REMINDER FOR DESMOND: PASS IN QUERYING USER OBJECT TO CHECK VALIDITY
class UserController:
    @staticmethod
    def retrieve_all_users():
        return E.UserEntity().retrieve_all()
        
    @staticmethod
    def retrieve_user(user_id):
        return E.UserEntity().retrieve_by_id(user_id)

    @staticmethod
    def login(email, password):
        if email == "" or password == "":
            return False
        return E.UserEntity().validate_login(email, password)

    @staticmethod
    def save_user(user_id, email, name, phone_number, address, role):
        user_id = int(user_id)
        # email_check = E.UserEntity().retrieve_all_by_email(email)
        print(f'{user_id = }')
        # if email_check:
        #     if len(email_check) > 1 or email_check[0].object_id != user_id:
        #         raise IntegrityError(f'Email must be unique.')
        # phone_number_check = E.UserEntity().retrieve_all_by_phone_number(phone_number)
        # if phone_number_check:
        #     if len(phone_number_check) > 1 or phone_number_check[0].object_id != user_id:
        #         raise IntegrityError(f'Phone number must be unique')
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
        if UserController.check_email_match(email):
            raise IntegrityError(f'Email must be unique.')
        if UserController.check_phone_number_match(phone_number):
            raise IntegrityError(f'Phone number must be unique')
        E.UserEntity().create('User', email=email, name=name, phone_number=phone_number, address=address, role=role, password=password)

    @staticmethod
    def check_email_match(email, user_id=None):
        email_check = E.UserEntity().retrieve_all_by_email(email)
        # If email_check list has elements and user_id is valid
        if email_check and user_id:
            if len(email_check) > 1 or email_check[0].object_id != user_id:
                return True
        return False

    @staticmethod
    def check_phone_number_match(phone_number, user_id=None):
        phone_number_check = E.UserEntity().retrieve_all_by_email(phone_number)
        # If phone_number_check list has elements and user_id is valid
        if phone_number_check and user_id:
            if len(phone_number_check) > 1 or phone_number_check[0].object_id != user_id:
                return True
        return False

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
    def retrieve_medicine(medicine_id):
        return MedicineController.e.retrieve_by_id(medicine_id)

    @staticmethod
    def retrieve_all_medicines():
        return MedicineController.e.retrieve_all()


class MedicineQuantityController:
    e = E.MedicineQuantityEntity()

    @staticmethod
    def retrieve_prescription_medicines(prescription_id):
        return MedicineQuantityController.e.retrieve_by_prescription(prescription_id)

    @staticmethod
    def retrieve_cart_medicines(cart_id):
        return MedicineQuantityController.e.retrieve_by_cart(cart_id)
