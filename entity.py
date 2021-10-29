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
            prescriptions.append(Prescription().set_id(prescription[2]))
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

    def set_id(self, prescription_id):
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
            self.get_status_string(result[0][5])
            self.prescription_details = result[0][6]

    def retrieve_record(self):
        return self.prescription_details

    def get_status_string(self, status):
        self.status = 'Collected' if status == 1 else 'Not collected'

    @staticmethod
    def get_all():
        query = f"SELECT * FROM PRESCRIPTION"
        db_obj = db_helper.db_helper()
        result = db_obj.query_db(query)
        items = []
        for item in result:
            p = Prescription()
            p.date = item[0]
            p.code = item[1]
            p.prescription_id = item[2]
            p.patient_id = item[3]
            p.doctor_id = item[4]
            p.get_status_string(item[5])
            p.prescription_details = item[6]
            items.append(p)
        print(items)
        return items

