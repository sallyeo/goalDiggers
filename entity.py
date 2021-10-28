class User:
    def validateLogin(self, email, password):
        if email == "sally" and password == "123":
            return True, "1"
        else:
            return False, ""

    def retrieveUserInfo(self, userNo):  # need to pass in user email not userID?
        listOfUsers = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]
        return listOfUsers

    def retrieveSpecificUser(self, userNo):
        # select lineEdit from database
        listofdetails = [1, 2, 3, 4, 5]
        return listofdetails


class Prescription:
    def retrieveUserPrescriptions(self, patientNo):     # pass in patientID
        listOfPrescriptions =[[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]
        return listOfPrescriptions

    def retrieveRecord(self, Code):     # pass in String Code
        # select lineEdit from database
        listofdetails = [1, 2, 3, 4]

        # select medicine from database
        listofmeds = [["001", 10], ["002", 199], ["005", 90]]

        return listofdetails, listofmeds
