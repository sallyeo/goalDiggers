import entity as E


class Session:
    user = None
    args = ()
    kwargs = {}

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.args = args
        self.kwargs = kwargs


class LoginController:
    def checkLoginInput(self, email, password):
        # check if password is empty
        if email == "" or password == "":
            return False
        return E.User.validate_login(email, password)


# REMINDER FOR DESMOND: PASS IN QUERYING USER OBJECT TO CHECK VALIDITY
class UserController:
    @staticmethod
    def retrieve_patient_prescriptions(patient_id):
        user_entity = E.User()
        user_entity.set_id(patient_id)
        return user_entity.retrieve_user_prescriptions()

    @staticmethod
    def retrieve_all_users():
        return E.User.retrieve_all_users()
        
    @staticmethod
    def retrieve_user(user_id):
        return E.User().retrieve_user(user_id)


class PrescriptionController:
    @staticmethod
    def retrieve_all_prescriptions():
        return E.Prescription.get_all_prescriptions()

    @staticmethod
    def retrieve_prescription(code):
        return E.Prescription().get_prescription(code)
