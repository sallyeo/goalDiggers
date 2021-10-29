import db_helper


class User:
    user_type_id = ''

    def set_id(self, user_type_id):
        self.user_type_id = user_type_id

    def validate_login(self, email, password, usertype):
        validation_query = f"SELECT * FROM USERS WHERE email = '{email}' AND PASSWORD = '{password}' AND USER_TYPE = '{usertype}'"
        # validate input
        db_obj = db_helper.db_helper()  # call helper object
        result = db_obj.query_db(validation_query)  # retrieve query results
        if len(result) == 1:
            return True, result[0][1]
        return False, ""

    def retrieveUserInfo(self, userNo):  # need to pass in user email not userID?
        listOfUsers = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]
        return listOfUsers

    def retrieveSpecificUser(self, userNo):
        # select lineEdit from database
        listofdetails = [1, 2, 3, 4, 5]
        return listofdetails

    def retrieve_user_prescriptions(self):
        prescriptions = []
        print(self.user_type_id)
        query = f"SELECT * FROM PRESCRIPTION WHERE patient_id = '{self.user_type_id}'"
        db_obj = db_helper.db_helper()  # call helper object
        result = db_obj.query_db(query)
        for prescription in result:
            prescriptions.append(Prescription(prescription[2]))
        print(prescriptions)
        return prescriptions


class Prescription:
    date = ''
    code = ''
    prescription_id = ''
    patient_id = ''
    doctor_id = ''
    status = None
    prescription_details = ''

    def __init__(self, prescription_id):
        query = f"SELECT * FROM PRESCRIPTION WHERE prescription_id = '{prescription_id}'"
        db_obj = db_helper.db_helper()  # call helper object
        result = db_obj.query_db(query)
        print(result)
        if len(result) > 0:
            self.date = result[0][0]
            self.code = result[0][1]
            self.prescription_id = result[0][2]
            self.patient_id = result[0][3]
            self.doctor_id = result[0][4]
            self.status = 'Collected' if result[0][5] is 1 else 'Not collected'
            self.prescription_details = result[0][6]

    def retrieveRecord(self, Code):  # pass in String Code
        # select lineEdit from database
        listofdetails = [1, 2, 3, 4]

        # select medicine from database
        listofmeds = [["001", 10], ["002", 199], ["005", 90]]

        return listofdetails, listofmeds
