import db_helper


class User:
    id = -1
    user_type_id = ''
    name = ''
    email = ''
    address = ''
    phone_number = ''
    user_type = ''

    def set_id(self, user_type_id):
        self.user_type_id = user_type_id

    def set_values(self, id, user_type_id, name, email, address, phone_number, user_type):
        self.id = int(id)
        self.user_type_id = user_type_id
        self.name = name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.user_type = user_type

    @staticmethod
    def validate_login(email, password):
        validation_query = f"SELECT * FROM USERS WHERE email = '{email}' AND PASSWORD = '{password}'"
        # validate input
        db_obj = db_helper.db_helper()  # call helper object
        result = db_obj.query_db(validation_query)  # retrieve query results
        if len(result) == 1:
            r = result[0]
            u = User()
            u.set_values(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
            return u
        return False

    def retrieveUserInfo(self, userNo):  # need to pass in user email not userID?
        listOfUsers = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]]
        return listOfUsers

    def retrieveSpecificUser(self, userNo):
        # select lineEdit from database
        listofdetails = [1, 2, 3, 4, 5]
        return listofdetails

    def retrieve_user(self, user_id):
        query = f"SELECT * FROM USERS WHERE user_type_id = '{user_id}'"
        db_obj = db_helper.db_helper()
        results = db_obj.query_db(query)
        if len(results) > 0:
            r = results[0]
            self.set_values(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
            return self
        return False

    # @staticmethod
    # def retrieve_all_users(self):
    #     query = f"SELECT * FROM USERS"
    #     db_obj = db_helper.db_helper()
    #     results = db_obj.query_db(query)
    #     for user in results:
    #         u = User()
    #         u.set_id()

    def retrieve_user_prescriptions(self):
        prescriptions = []
        print(self.user_type_id)
        query = f"SELECT * FROM PRESCRIPTION WHERE patient_id = '{self.user_type_id}'"
        db_obj = db_helper.db_helper()  # call helper object
        results = db_obj.query_db(query)
        for prescription in results:
            print(f'presciption: {prescription}')
            p = Prescription()
            p.set_id(prescription[2])
            prescriptions.append(p)
        print(prescriptions)
        return prescriptions

    @staticmethod
    def retrieve_all_users():
        query = f"SELECT * FROM USERS"
        db_obj = db_helper.db_helper()
        result = db_obj.query_db(query)
        users = []
        for user in result:
            u = User()
            u.set_values(user[0], user[1], user[2], user[3], user[4], user[5], user[6])
            users.append(u)
        return users

    def __str__(self):
        return f'Patient ID: {self.user_type_id}'


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
        db_obj = db_helper.db_helper()
        result = db_obj.query_db(query)
        print(result)
        if len(result) > 0:
            r = result[0]
            self.set_values(r[0], r[1], r[2], r[3], r[4], r[5], r[6])

    def set_values(self, date, code, prescription_id, patient_id, doctor_id, status, prescription_details):
        self.date = date
        self.code = code
        self.prescription_id = prescription_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.set_status_string(status)
        self.prescription_details = prescription_details

    def retrieve_record(self):
        return self.prescription_details

    def set_status_string(self, status):
        self.status = 'Collected' if status == 1 else 'Not collected'

    def get_prescription(self, code):
        query = f"SELECT * FROM PRESCRIPTION WHERE string_code = '{code}'"
        db_obj = db_helper.db_helper()
        result = db_obj.query_db(query)
        if len(result) > 0:
            r = result[0]
            self.set_values(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
            return self
        return False

    @staticmethod
    def get_all_prescriptions():
        query = f"SELECT * FROM PRESCRIPTION"
        db_obj = db_helper.db_helper()
        result = db_obj.query_db(query)
        items = []
        for item in result:
            p = Prescription()
            p.set_values(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
            items.append(p)
        print(items)
        return items

    def __str__(self):
        return f'Prescription: {self.prescription_id}'


class Medicine:
    id = -1
    name = ''
