import entity as E


class LoginController:
    def checkLoginInput(self, email, password, usertype):
        # check if password is empty
        if email == "" or password == "":
            return False, ""
        else:
            loginEntity = E.User()
            # controller calling entity
            validation, userNo = loginEntity.validate_login(email, password, usertype)
            if validation:
                return True, userNo
            else:
                return False, ""


class RetrieveUserInfoController:
    def retrieveUserInfo(self, user_no):  # need to pass in user email not the ptID?
        # controller calling entity
        retrieveUserEntity = E.User()
        retrieveUserEntity.set_id(user_no)
        listOfUsers = retrieveUserEntity.retrieveUserInfo(user_no)
        return listOfUsers


class RetrieveSpecificUserController:
    def retrieveSpecificUserInfo(self, user_no):
        # controller calling entity
        retrieveSpecificUserEntity = E.User()
        retrieveSpecificUserEntity.set_id(user_no)
        listOfUserInfo = retrieveSpecificUserEntity.retrieveSpecificUser()
        return listOfUserInfo


class RetrieveRecordsController:
    def retrieveUserPrescriptions(self, patient_no):
        # controller calling entity
        retrieve_records_entity = E.User()
        retrieve_records_entity.set_id(patient_no)
        listOfPrescriptions = retrieve_records_entity.retrieve_user_prescriptions()
        return listOfPrescriptions


class Retrieve1RecordController:
    def retrieveRecord(self, StringCode):
        # controller calling entity
        retrieve1RecordEntity = E.Prescription()
        listOfDetails , listOfMeds = retrieve1RecordEntity.retrieve_record(StringCode)
        return listOfDetails, listOfMeds


class RetrieveAllRecords:
    @staticmethod
    def retrieve_records():
        records = E.Prescription.get_all()
        return records
