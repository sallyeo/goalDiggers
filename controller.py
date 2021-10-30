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

# class LoginController:
#     def checkLoginInput(self, email, password):
#         # check if password is empty
#         if email == "" or password == "":
#             return False
#         return E.User.validate_login(email, password)


# REMINDER FOR DESMOND: PASS IN QUERYING USER OBJECT TO CHECK VALIDITY
class UserController:
    # @staticmethod
    # def retrieve_patient_prescriptions(patient_id):
    #     # user_entity = E.User()
    #     # user_entity.set_id(patient_id)
    #     # return user_entity.retrieve_user_prescriptions()

    @staticmethod
    def retrieve_all_users():
        # return E.User.retrieve_all_users()
        return E.UserEntity().retrieve_all()
        
    @staticmethod
    def retrieve_user(user_id):
        # return E.User().retrieve_user(user_id)
        return E.UserEntity().retrieve_one(user_id)

    @staticmethod
    def login(email, password):
        if email == "" or password == "":
            return False
        return E.UserEntity().validate_login(email, password)


class PrescriptionController:
    e = E.PrescriptionEntity()

    @staticmethod
    def retrieve_all_prescriptions():
        # return E.Prescription.get_all_prescriptions()
        return PrescriptionController.e.retrieve_all()

    @staticmethod
    def retrieve_prescription(code):
        # return E.Prescription().retrieve_prescription(code)
        return PrescriptionController.e.retrieve_one(code)

    @staticmethod
    def retrieve_patient_prescriptions(patient_id):
        return PrescriptionController.e.retrieve_by_fk(patient_id)


class MedicineController:
    e = E.MedicineEntity()

    @staticmethod
    def retrieve_medicine(medicine_id):
        return MedicineController.e.retrieve_one(medicine_id)

    @staticmethod
    def retrieve_all_medicines():
        return MedicineController.e.retrieve_all()

    # @staticmethod
    # def retrieve_prescription_medicines(prescription_id):
    #     return MedicineController.e.
