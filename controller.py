import entity as E

class LoginController:
    def checkLoginInput(self, email, password, usertype):
        # check if password is empty
        if email == "" or password == "":
            return False, ""
        else:
            loginEntity = E.User()
            # controller calling entity
            validation, userNo = loginEntity.validateLogin(email, password, usertype)
            if validation:
                return True, userNo
            else:
                return False, ""


class RetrieveUserInfoController:
    def retrieveUserInfo(self, userNo):  # need to pass in user email not the ptID?
        # controller calling entity
        retrieveUserEntity = E.User()
        listOfUsers = retrieveUserEntity.retrieveUserInfo(userNo)
        return listOfUsers

class RetrieveSpecificUserController:
    def retrieveSpecificUserInfo(self, userNo):
        # controller calling entity
        retrieveSpecificUserEntity = E.User()
        listOfUserInfo = retrieveSpecificUserEntity.retrieveSpecificUser(userNo)
        return listOfUserInfo

class RetrieveRecordsController:
    def retrieveUserPrescriptions(self, patientNo):
        # controller calling entity
        RetrieveRecordsEntity = E.Prescription()
        listOfPrescriptions = RetrieveRecordsEntity.retrieveUserPrescriptions(patientNo)
        return listOfPrescriptions


class Retrieve1RecordController:
    def retrieveRecord(self, StringCode):
        # controller calling entity
        retrieve1RecordEntity = E.Prescription()
        listOfDetails , listOfMeds = retrieve1RecordEntity.retrieveRecord(StringCode)
        return listOfDetails, listOfMeds
