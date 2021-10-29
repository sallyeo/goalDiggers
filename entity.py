import db_helper


class User:
    def validateLogin(self, email, password, usertype):

        validation_query = "SELECT * FROM USERS WHERE email = '{email}' AND PASSWORD = '{password}' AND USER_TYPE = '{usertype}'".format(
            email=email,
            password=password, usertype=usertype)
        # validate input
        db_obj = db_helper.db_helper()  # call helper object
        result = db_obj.query_db(validation_query)  # retrieve query results

        if len(result) == 1:
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
    def retrieveUserPrescriptions(self, patientNo):  # pass in patientID
        listOfPrescriptions = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]
        return listOfPrescriptions

    def retrieveRecord(self, Code):  # pass in String Code
        # select lineEdit from database
        listofdetails = [1, 2, 3, 4]

        # select medicine from database
        listofmeds = [["001", 10], ["002", 199], ["005", 90]]

        return listofdetails, listofmeds
