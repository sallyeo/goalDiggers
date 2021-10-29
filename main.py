import sys, res, controller
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QMessageBox, QTableWidgetItem,QAbstractItemView
from PyQt5.uic import loadUi
import controller as C

# Variables
global g_user
global StringCode
global g_name

status_dict = {
    'Not collected': 2,
    'Collected': 1
}

role_dict = {
    'Admin': 0,
    'Patient': 1,
    'Doctor': 2,
    'Pharmacist': 3,
}


class LoginView(QDialog):
    def __init__(self):
        super(LoginView, self).__init__()
        loadUi("loginDialog.ui", self)  # load the ui file
        self.loginButton.clicked.connect(self.login)    # loginButton
        self.registerButton.clicked.connect(self.goToCreate) # registerButton

    def login(self):
        email = self.email.text()   # get email from user input
        password = self.password.text()     # get password from user input
        usertype = self.userMenu.currentText()

        # boundary calling controller
        loginControl = C.LoginController()
        user = loginControl.checkLoginInput(email, password)
        if user:   # if input valid
            global g_user
            g_user = user
            # C.Session(user)
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Login success")
            msgbox.setText("WELCOME TO GD PRESCRIPTION")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()
            if user.user_type == "Doctor":
                doctor_home = DoctorHome()
                widget.addWidget(doctor_home)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif user.user_type == "Patient":
                patient_home = PatientHome()
                widget.addWidget(patient_home)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif user.user_type == "Pharmacist":
                pharmacist_home = PharmacistHome()
                widget.addWidget(pharmacist_home)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                admin_home = AdminHome()
                widget.addWidget(admin_home)
                widget.setCurrentIndex(widget.currentIndex() + 1)
        else:   # if input invalid
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Login fail")
            msgbox.setText("INVALID CREDENTIALS INPUT!")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()

    def goToCreate(self):
        registerAcc = Register()
        widget.addWidget(registerAcc)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Home(QMainWindow):
    user_controller = C.UserController()

    def __init__(self, window, column_sizes=None):
        super(Home, self).__init__()
        if column_sizes is None:
            column_sizes = [100, 290, 90, 70, 70, 180]
        loadUi(window, self)
        widget.setFixedSize(930,750)
        for i in range(len(column_sizes)):
            self.table.setColumnWidth(i, column_sizes[i])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.cellClicked.connect(self.view_prescription)
        self.logoutButton.clicked.connect(self.logout_app)
        # self.viewButton.clicked.connect(self.viewPrescription)
        self.show_records()

    def display_records(self, records):
        self.table.setRowCount(len(records))
        for count, item in enumerate(records):
            self.table.setItem(count, 0, QTableWidgetItem(item.date))
            self.table.setItem(count, 1, QTableWidgetItem(item.code))
            self.table.setItem(count, 2, QTableWidgetItem(item.prescription_id))
            self.table.setItem(count, 3, QTableWidgetItem(item.patient_id))
            self.table.setItem(count, 4, QTableWidgetItem(item.doctor_id))
            self.table.setItem(count, 5, QTableWidgetItem(item.status))

    def display_users(self, users):
        self.table.setRowCount(len(users))
        for count, user in enumerate(users):
            self.table.setItem(count, 0, QTableWidgetItem(user.user_type_id))
            self.table.setItem(count, 1, QTableWidgetItem(user.name))
            self.table.setItem(count, 2, QTableWidgetItem(user.email))
            self.table.setItem(count, 3, QTableWidgetItem(user.address))
            self.table.setItem(count, 4, QTableWidgetItem(user.phone_number))
            self.table.setItem(count, 5, QTableWidgetItem(user.user_type))

    def view_prescription(self):
        row = self.table.currentRow()
        global StringCode
        print('view_prescription called')
        StringCode = self.table.item(row, 1).text()

    def view_user(self):
        row = self.table.currentRow()
        global g_name
        g_name = C.UserController.retrieve_user(self.table.item(row, 0).text())
        print(g_name)

    def logout_app(self):
        # calling LoginView() of boundary class
        ret_to_login = LoginView()
        widget.addWidget(ret_to_login)
        widget.setCurrentIndex(widget.currentIndex()+1)


class PatientHome(Home):
    def __init__(self):
        super(PatientHome, self).__init__('patientMainWindow.ui')
        
    def show_records(self):
        self.idLine.setText(g_user.user_type_id)
        self.nameLine.setText(g_user.name)
        self.emailLine.setText(g_user.email)
        self.addressLine.setText(g_user.address)
        self.telLine.setText(g_user.phone_number)
        self.display_records(self.user_controller.retrieve_patient_prescriptions(g_user.user_type_id))

    def view_prescription(self):
        super(PatientHome, self).view_prescription()
        prescription = PatientViewPrescription()
        widget.addWidget(prescription)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DoctorHome(Home):
    def __init__(self):
        super(DoctorHome, self).__init__('doctorMainWindow.ui')
    
    def show_records(self):
        # boundary calling controller
        # prescriptions = C.RetrieveAllRecords.retrieve_records()
        prescriptions = C.PrescriptionController.retrieve_all_prescriptions()
        self.display_records(prescriptions)

    def view_prescription(self):
        super(DoctorHome, self).view_prescription()
        prescription = DoctorViewPrescription()
        widget.addWidget(prescription)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class PharmacistHome(Home):
    def __init__(self):
        super(PharmacistHome, self).__init__('pharmacistMainWindow.ui')
    
    def show_records(self):
        # boundary calling controller
        # prescriptions = C.RetrieveAllRecords.retrieve_records()
        prescriptions = C.PrescriptionController.retrieve_all_prescriptions()
        self.display_records(prescriptions)

    def view_prescription(self):
        super(PharmacistHome, self).view_prescription()
        prescription = PharmacistViewPrescription()
        widget.addWidget(prescription)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AdminHome(Home):
    def __init__(self):
        super(AdminHome, self).__init__('adminMainWindow.ui', [50, 100, 100, 150, 100, 100])
        self.table.cellClicked.connect(self.view_user)
        
    def show_records(self):
        users = self.user_controller.retrieve_all_users()
        self.display_users(users)

    def view_user(self):
        super(AdminHome, self).view_user()
        view_user_info = AdminViewUser()
        widget.addWidget(view_user_info)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# class PatientHome(QMainWindow):
#     def __init__(self):
#         super(PatientHome, self).__init__()
#         loadUi("patientMainWindow.ui", self)
#         widget.setFixedSize(930,750)
#         self.patientMainTable.setColumnWidth(0, 100)
#         self.patientMainTable.setColumnWidth(1, 290)
#         self.patientMainTable.setColumnWidth(2, 90)
#         self.patientMainTable.setColumnWidth(3, 70)
#         self.patientMainTable.setColumnWidth(4, 70)
#         self.patientMainTable.setColumnWidth(5, 180)
#         self.patientMainTable.setSelectionBehavior(QAbstractItemView.SelectRows)
#         self.patientMainTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
#         self.patientMainTable.verticalHeader().setVisible(False)
#         self.patientMainTable.cellClicked.connect(self.viewPrescription)
#         self.logoutButton.clicked.connect(self.logoutApp)
#         # self.viewButton.clicked.connect(self.viewPrescription)
#         self.showRecords()
#
#     def showRecords(self):      # to show list of prescriptions
#         retrieveRecordsController = C.RetrieveRecordsController()
#         # boundary calling controller
#         prescriptions = retrieveRecordsController.retrieveUserPrescriptions(UserNo)
#         for count, item in enumerate(prescriptions):
#             self.patientMainTable.insertRow(count)
#             self.patientMainTable.setItem(count, 0, QTableWidgetItem(item.date))
#             self.patientMainTable.setItem(count, 1, QTableWidgetItem(item.code))
#             self.patientMainTable.setItem(count, 2, QTableWidgetItem(item.prescription_id))
#             self.patientMainTable.setItem(count, 3, QTableWidgetItem(item.patient_id))
#             self.patientMainTable.setItem(count, 4, QTableWidgetItem(item.doctor_id))
#             self.patientMainTable.setItem(count, 5, QTableWidgetItem(item.status))
#
#     def viewPrescription(self):
#         row = self.patientMainTable.currentRow()
#         global StringCode
#         StringCode = self.patientMainTable.item(row, 1).text()
#         toViewPrescription = PatientViewPrescription()
#         widget.addWidget(toViewPrescription)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
#
#     def logoutApp(self):
#         msgbox = QMessageBox()
#         msgbox.setWindowTitle("Logout")
#         msgbox.setText("Logging out")
#         msgbox.setStandardButtons(QMessageBox.Ok)
#         msgbox.exec_()
#         # calling LoginView() of boundary class
#         RetToLogin = LoginView()
#         widget.addWidget(RetToLogin)
#         widget.setCurrentIndex(widget.currentIndex()+1)


class ViewPrescription(QDialog):
    def __init__(self, window, widget_size=None, column_sizes=None):
        super(ViewPrescription, self).__init__()
        if widget_size is None:
            widget_size = [730, 650]
        if column_sizes is None:
            column_sizes = [200, 60, 351]
        loadUi(window, self)
        widget.setFixedSize(widget_size[0], widget_size[1])
        for i in range(len(column_sizes)):
            self.table.setColumnWidth(i, column_sizes[i])
        self.backButton.clicked.connect(self.to_home)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.display_details()

    def display_details(self):
        print("string Code passed: ", StringCode)
        prescriptions = C.PrescriptionController.retrieve_prescription(StringCode)
        print(prescriptions)
        self.PrescriptionIdLine.setText(prescriptions.prescription_id)
        self.patientIdLine.setText(prescriptions.patient_id)
        self.doctorIdLine.setText(prescriptions.doctor_id)
        self.prescriptionDateLine.setText(prescriptions.date)
        self.statusMenu.setCurrentIndex(1 if prescriptions.status == 'Collected' else 0)
        # for rowNo, rowRecords in enumerate(listofmeds):
        #     self.patientViewPresTable.insertRow(rowNo)
        #     for colNo, record in enumerate(rowRecords):
        #         self.patientViewPresTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))


class PatientViewPrescription(ViewPrescription):
    def __init__(self):
        super(PatientViewPrescription, self).__init__('patientViewPrescription.ui')

    def to_home(self):
        home = PatientHome()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DoctorViewPrescription(ViewPrescription):
    def __init__(self):
        super(DoctorViewPrescription, self).__init__('doctorViewPrescription.ui')

    def to_home(self):
        home = DoctorHome()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class PharmacistViewPrescription(ViewPrescription):
    def __init__(self):
        super(PharmacistViewPrescription, self).__init__('pharmacistViewPrescription.ui')

    def to_home(self):
        home = PharmacistHome()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ViewUser(QDialog):
    def __init__(self, window):
        super(ViewUser, self).__init__()
        loadUi(window, self)
        widget.setFixedSize(730, 650)
        self.backButton.clicked.connect(self.to_home)
        self.display_details()

    def display_details(self):
        print("User No passed: ", g_name)
        user = C.UserController.retrieve_user(g_name.user_type_id)
        print(user.user_type)
        print(role_dict[user.user_type])
        self.userMenu.setCurrentIndex(role_dict[user.user_type])
        self.idLine.setText(str(user.id))
        self.nameLine.setText(user.name)
        self.emailLine.setText(user.email)
        self.addressLine.setText(user.address)
        self.telLine.setText(user.phone_number)


class AdminViewUser(ViewUser):
    def __init__(self):
        super(AdminViewUser, self).__init__('adminEditUser.ui')

    def to_home(self):
        home = AdminHome()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# class PatientViewPrescription(QDialog):
#     def __init__(self):
#         super(PatientViewPrescription, self).__init__()
#         loadUi("patientViewPrescription.ui", self)
#         widget.setFixedSize(730, 650)
#         self.patientViewPresTable.setColumnWidth(0, 200)
#         self.patientViewPresTable.setColumnWidth(1, 60)
#         self.patientViewPresTable.setColumnWidth(2, 351)
#         self.backButton.clicked.connect(self.toHome)
#         self.patientViewPresTable.setSelectionBehavior(QAbstractItemView.SelectRows)
#         self.patientViewPresTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
#         self.patientViewPresTable.verticalHeader().setVisible(False)
#         self.displayDetails()
#
#     def displayDetails(self):
#         print("string Code passed: ", StringCode)
#         # Retrieve1RecordControl = C.Retrieve1RecordController()
#         # listofdetails, listofmeds = Retrieve1RecordControl.retrieveRecord(StringCode)
#         prescriptions = C.PrescriptionController.retrieve_prescription(StringCode)
#         print(prescriptions)
#         self.PrescriptionIdLine.setText(prescriptions.prescription_id)
#         self.patientIdLine.setText(prescriptions.patient_id)
#         self.doctorIdLine.setText(prescriptions.doctor_id)
#         self.prescriptionDateLine.setText(prescriptions.date)
#         # self.PrescriptionIdLine.setText(str(listofdetails[0]))
#         # self.patientIdLine.setText(str(listofdetails[1]))
#         # self.doctorIdLine.setText(str(listofdetails[2]))
#         # self.prescriptionDateLine.setText(str(listofdetails[3]))
#         self.statusMenu.currentText()
#         # for rowNo, rowRecords in enumerate(listofmeds):
#         #     self.patientViewPresTable.insertRow(rowNo)
#         #     for colNo, record in enumerate(rowRecords):
#         #         self.patientViewPresTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))
#
#     def toHome(self):
#         toHome = PatientHome()
#         widget.addWidget(toHome)
#         widget.setCurrentIndex(widget.currentIndex() + 1)


# class DoctorHome(QMainWindow):
#     def __init__(self):
#         super(DoctorHome, self).__init__()
#         loadUi("doctorMainWindow.ui", self)
#         widget.setFixedSize(930, 750)
#         self.doctorMainTable.setColumnWidth(0, 100)
#         self.doctorMainTable.setColumnWidth(1, 290)
#         self.doctorMainTable.setColumnWidth(2, 90)
#         self.doctorMainTable.setColumnWidth(3, 70)
#         self.doctorMainTable.setColumnWidth(4, 70)
#         self.doctorMainTable.setColumnWidth(5, 180)
#         self.doctorMainTable.setSelectionBehavior(QAbstractItemView.SelectRows)
#         self.doctorMainTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
#         self.doctorMainTable.verticalHeader().setVisible(False)
#         self.doctorMainTable.cellClicked.connect(self.viewPrescription)
#         self.logoutButton.clicked.connect(self.logoutApp)
#         # self.viewButton.clicked.connect(self.viewPrescription)
#         self.showRecords()
#
#     def showRecords(self):
#         retrieveRecordsController = C.RetrieveRecordsController()
#         prescriptions = retrieveRecordsController.retrieveUserPrescriptions(UserNo)
#         # for rowNo, rowRecords in enumerate(listOfRecords):
#         #     self.doctorMainTable.insertRow(rowNo)
#         #     for colNo, record in enumerate(rowRecords):
#         #         self.doctorMainTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))
#
#
#     def viewPrescription(self):
#         row = self.table.currentRow()
#         global StringCode
#         StringCode = self.table.item(row, 1).text()
#         toViewPrescription = DoctorViewPrescription()
#         widget.addWidget(toViewPrescription)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
#
#     def logoutApp(self):
#         msgbox = QMessageBox()
#         msgbox.setWindowTitle("Logout")
#         msgbox.setText("Logging out")
#         msgbox.setStandardButtons(QMessageBox.Ok)
#         msgbox.exec_()
#         # calling LoginView() of boundary class
#         RetToLogin = LoginView()
#         widget.addWidget(RetToLogin)
#         widget.setCurrentIndex(widget.currentIndex()+1)


# class DoctorViewPrescription(QDialog):
#     def __init__(self):
#         super(DoctorViewPrescription, self).__init__()
#         loadUi("doctorViewPrescription.ui", self)
#         widget.setFixedSize(730, 650)
#         self.doctorViewPresTable.setColumnWidth(0, 200)
#         self.doctorViewPresTable.setColumnWidth(1, 90)
#         self.doctorViewPresTable.setColumnWidth(2, 321)
#         self.backButton.clicked.connect(self.toHome)
#         self.doctorViewPresTable.setSelectionBehavior(QAbstractItemView.SelectRows)
#         self.doctorViewPresTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
#         self.doctorViewPresTable.verticalHeader().setVisible(False)
#         self.displayDetails()
#
#     def displayDetails(self):
#         print("string Code passed: ", StringCode)
#         Retrieve1RecordControl = C.Retrieve1RecordController()
#         listofdetails, listofmeds = Retrieve1RecordControl.retrieveRecord(StringCode)
#         self.PrescriptionIdLine.setText(str(listofdetails[0]))
#         self.patientIdLine.setText(str(listofdetails[1]))
#         self.doctorIdLine.setText(str(listofdetails[2]))
#         self.prescriptionDateLine.setText(str(listofdetails[3]))
#         self.statusMenu.currentText()
#         for rowNo, rowRecords in enumerate(listofmeds):
#             self.doctorViewPresTable.insertRow(rowNo)
#             for colNo, record in enumerate(rowRecords):
#                 self.doctorViewPresTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))
#
#     def toHome(self):
#         toHome = DoctorHome()
#         widget.addWidget(toHome)
#         widget.setCurrentIndex(widget.currentIndex() + 1)


# class PharmacistHome(QMainWindow):
#     def __init__(self):
#         super(PharmacistHome, self).__init__()
#         loadUi("pharmacistMainWindow.ui", self)
#         widget.setFixedSize(930, 750)
#         self.pharmacistMainTable.setColumnWidth(0, 100)
#         self.pharmacistMainTable.setColumnWidth(1, 290)
#         self.pharmacistMainTable.setColumnWidth(2, 90)
#         self.pharmacistMainTable.setColumnWidth(3, 70)
#         self.pharmacistMainTable.setColumnWidth(4, 70)
#         self.pharmacistMainTable.setColumnWidth(5, 180)
#         self.pharmacistMainTable.setSelectionBehavior(QAbstractItemView.SelectRows)
#         self.pharmacistMainTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
#         self.pharmacistMainTable.verticalHeader().setVisible(False)
#         self.pharmacistMainTable.cellClicked.connect(self.viewPrescription)
#         self.logoutButton.clicked.connect(self.logoutApp)
#         self.showRecords()
#
#     def showRecords(self):
#         retrieveRecordsController = C.RetrieveRecordsController()
#         listOfRecords = retrieveRecordsController.retrieveUserPrescriptions(UserNo)
#         for rowNo, rowRecords in enumerate(listOfRecords):
#             self.pharmacistMainTable.insertRow(rowNo)
#             for colNo, record in enumerate(rowRecords):
#                 self.pharmacistMainTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))
#
#     def viewPrescription(self):
#         row = self.pharmacistMainTable.currentRow()
#         global StringCode
#         StringCode = self.pharmacistMainTable.item(row, 1).text()
#         toViewPrescription = PharmacistViewPrescription()
#         widget.addWidget(toViewPrescription)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
#
#     def logoutApp(self):
#         msgbox = QMessageBox()
#         msgbox.setWindowTitle("Logout")
#         msgbox.setText("Logging out")
#         msgbox.setStandardButtons(QMessageBox.Ok)
#         msgbox.exec_()
#         RetToLogin = LoginView()
#         widget.addWidget(RetToLogin)
#         widget.setCurrentIndex(widget.currentIndex()+1)


# class PharmacistViewPrescription(QDialog):
#     def __init__(self):
#         super(PharmacistViewPrescription, self).__init__()
#         loadUi("pharmacistViewPrescription.ui", self)
#         widget.setFixedSize(730, 650)
#         self.pharmacistViewPresTable.setColumnWidth(0, 200)
#         self.pharmacistViewPresTable.setColumnWidth(1, 90)
#         self.pharmacistViewPresTable.setColumnWidth(2, 321)
#         self.backButton.clicked.connect(self.toHome)
#         self.pharmacistViewPresTable.setSelectionBehavior(QAbstractItemView.SelectRows)
#         self.pharmacistViewPresTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
#         self.pharmacistViewPresTable.verticalHeader().setVisible(False)
#         self.displayDetails()
#
#     def displayDetails(self):
#         print("string Code passed: ", StringCode)
#         Retrieve1RecordControl = C.Retrieve1RecordController()
#         listofdetails, listofmeds = Retrieve1RecordControl.retrieveRecord(StringCode)
#         self.PrescriptionIdLine.setText(str(listofdetails[0]))
#         self.patientIdLine.setText(str(listofdetails[1]))
#         self.doctorIdLine.setText(str(listofdetails[2]))
#         self.prescriptionDateLine.setText(str(listofdetails[3]))
#         self.statusMenu.currentText()
#         for rowNo, rowRecords in enumerate(listofmeds):
#             self.pharmacistViewPresTable.insertRow(rowNo)
#             for colNo, record in enumerate(rowRecords):
#                 self.pharmacistViewPresTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))
#
#     def toHome(self):
#         toHome = PharmacistHome()
#         widget.addWidget(toHome)
#         widget.setCurrentIndex(widget.currentIndex() + 1)

class Register(QDialog):
    def __init__(self):
        super(Register, self).__init__()
        loadUi("registerDialog.ui", self)
        self.registerButton.clicked.connect(self.register)
        self.loginButton.clicked.connect(self.goToLogin)

    def register(self):
        email = self.email.text()
        if self.password.text() == self.confirmPass.text():
            password = self.password.text()
        print("Successfully registering in with email: ", email, "and password: ", password)
        self.goToLogin()

    def goToLogin(self):
        login = LoginView()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

#
# class AdminHome(QMainWindow):
#     def __init__(self):
#         super(AdminHome, self).__init__()
#         loadUi("adminMainWindow.ui", self)
#         widget.setFixedSize(740, 790)
#         widget.setWindowTitle("Admin Homepage")
#         self.table.setColumnWidth(0, 50)
#         self.table.setColumnWidth(1, 100)
#         self.table.setColumnWidth(2, 100)
#         self.table.setColumnWidth(3, 150)
#         self.table.setColumnWidth(4, 100)
#         self.table.setColumnWidth(4, 100)
#         self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
#         self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
#         self.table.verticalHeader().setVisible(False)
#         self.table.cellClicked.connect(self.view_user_info)
#         self.logoutButton.clicked.connect(self.logout_app)
#         self.show_records()
#
#     def show_records(self):      # to show list of users on admin homepage
#         retrieveUsersControl = C.RetrieveUserInfoController()
#         # boundary calling controller
#         users = retrieveUsersControl.retrieve_all_users()
#         # for rowNo, rowRecords in enumerate(listOfRecords):
#         #     self.adminMainTable.insertRow(rowNo)
#         #     for colNo, record in enumerate(rowRecords):
#         #         self.adminMainTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))
#         self.table.setRowCount(len(users))
#         for count, user in enumerate(users):
#             self.table.setItem(count, 0, QTableWidgetItem(user.user_type_id))
#             self.table.setItem(count, 1, QTableWidgetItem(user.name))
#             self.table.setItem(count, 2, QTableWidgetItem(user.email))
#             self.table.setItem(count, 3, QTableWidgetItem(user.address))
#             self.table.setItem(count, 4, QTableWidgetItem(user.phone_number))
#             self.table.setItem(count, 5, QTableWidgetItem(user.user_type))
#
#     def view_user_info(self):
#         row = self.table.currentRow()
#         # global UserNo
#         # UserNo = C.UserController.retrieve_user(self.table.item(row, 0).text())
#         toViewUserInfo = AdminViewUserInfo()
#         widget.addWidget(toViewUserInfo)
#         widget.setCurrentIndex(widget.currentIndex() + 1)
#
#     def logout_app(self):
#         msgbox = QMessageBox()
#         msgbox.setWindowTitle("Logout")
#         msgbox.setText("Logging out")
#         msgbox.setStandardButtons(QMessageBox.Ok)
#         msgbox.exec_()
#         RetToLogin = LoginView()
#         widget.addWidget(RetToLogin)
#         widget.setCurrentIndex(widget.currentIndex()+1)


# class AdminViewUserInfo(QDialog):
#     def __init__(self):
#         super(AdminViewUserInfo, self).__init__()
#         loadUi("adminEditUser.ui", self)
#         widget.setFixedSize(730, 650)
#         self.backButton.clicked.connect(self.toHome)
#         self.displayDetails()
#
#     def displayDetails(self):
#         print("User No passed: ", g_name)
#         Retrieve1UserControl = C.RetrieveSpecificUserController()
#         listofdetails = Retrieve1UserControl.retrieveSpecificUserInfo(g_name.user_type_id)
#         self.userMenu.currentText()
#         self.idLine.setText(str(listofdetails[0]))
#         self.nameLine.setText(str(listofdetails[1]))
#         self.emailLine.setText(str(listofdetails[2]))
#         self.addressLine.setText(str(listofdetails[3]))
#         self.telLine.setText(str(listofdetails[4]))
#
#     def toHome(self):
#         toHome = AdminHome()
#         widget.addWidget(toHome)
#         widget.setCurrentIndex(widget.currentIndex() + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = LoginView()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(600)
    widget.setFixedHeight(530)
    widget.show()
    app.exec()