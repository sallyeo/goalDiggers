import sys, res, controller
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QMessageBox, QTableWidgetItem,QAbstractItemView
from PyQt5.uic import loadUi
import controller as C
global UserNo
global StringCode


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
        Valid, userNo = loginControl.checkLoginInput(email, password, usertype)
        if Valid:   # if input valid
            global UserNo
            UserNo = userNo
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Login success")
            msgbox.setText("WELCOME TO GD PRESCRIPTION")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()
            if usertype == "Doctor":
                doctorHome = DoctorHome()
                widget.addWidget(doctorHome)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif usertype == "Patient":
                patientHome = PatientHome()
                widget.addWidget(patientHome)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif usertype == "Pharmacist":
                pharmacistHome = PharmacistHome()
                widget.addWidget(pharmacistHome)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                adminHome = AdminHome()
                widget.addWidget(adminHome)
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


class PatientHome(QMainWindow):
    def __init__(self):
        super(PatientHome, self).__init__()
        loadUi("patientMainWindow.ui", self)
        widget.setFixedSize(930,750)
        self.patientMainTable.setColumnWidth(0, 100)
        self.patientMainTable.setColumnWidth(1, 300)
        self.patientMainTable.setColumnWidth(2, 70)
        self.patientMainTable.setColumnWidth(3, 70)
        self.patientMainTable.setColumnWidth(4, 70)
        self.patientMainTable.setColumnWidth(5, 190)
        self.patientMainTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.patientMainTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.patientMainTable.verticalHeader().setVisible(False)
        self.patientMainTable.cellClicked.connect(self.viewPrescription)
        self.logoutButton.clicked.connect(self.logoutApp)
        # self.viewButton.clicked.connect(self.viewPrescription)
        self.showRecords()

    def showRecords(self):      # to show list of prescriptions
        retrieveRecordsController = C.RetrieveRecordsController()
        # boundary calling controller
        listOfRecords = retrieveRecordsController.retrieveUserPrescriptions(UserNo)
        for rowNo, rowRecords in enumerate(listOfRecords):
            self.patientMainTable.insertRow(rowNo)
            for colNo, record in enumerate(rowRecords):
                self.patientMainTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))

    def viewPrescription(self):
        row = self.patientMainTable.currentRow()
        global StringCode
        StringCode = self.patientMainTable.item(row, 1).text()
        toViewPrescription = PatientViewPrescription()
        widget.addWidget(toViewPrescription)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def logoutApp(self):
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Logout")
        msgbox.setText("Logging out")
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()
        # calling LoginView() of boundary class
        RetToLogin = LoginView()
        widget.addWidget(RetToLogin)
        widget.setCurrentIndex(widget.currentIndex()+1)


class PatientViewPrescription(QDialog):
    def __init__(self):
        super(PatientViewPrescription, self).__init__()
        loadUi("patientViewPrescription.ui", self)
        widget.setFixedSize(730, 650)
        self.patientViewPresTable.setColumnWidth(0, 200)
        self.patientViewPresTable.setColumnWidth(1, 90)
        self.patientViewPresTable.setColumnWidth(2, 321)
        self.backButton.clicked.connect(self.toHome)
        self.patientViewPresTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.patientViewPresTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.patientViewPresTable.verticalHeader().setVisible(False)
        self.displayDetails()

    def displayDetails(self):
        print("string Code passed: ", StringCode)
        Retrieve1RecordControl = C.Retrieve1RecordController()
        listofdetails, listofmeds = Retrieve1RecordControl.retrieveRecord(StringCode)
        self.PrescriptionIdLine.setText(str(listofdetails[0]))
        self.patientIdLine.setText(str(listofdetails[1]))
        self.doctorIdLine.setText(str(listofdetails[2]))
        self.prescriptionDateLine.setText(str(listofdetails[3]))
        self.statusMenu.currentText()
        for rowNo, rowRecords in enumerate(listofmeds):
            self.patientViewPresTable.insertRow(rowNo)
            for colNo, record in enumerate(rowRecords):
                self.patientViewPresTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))

    def toHome(self):
        toHome = PatientHome()
        widget.addWidget(toHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DoctorHome(QMainWindow):
    def __init__(self):
        super(DoctorHome, self).__init__()
        loadUi("doctorMainWindow.ui", self)
        widget.setFixedSize(930, 750)
        self.doctorMainTable.setColumnWidth(0, 100)
        self.doctorMainTable.setColumnWidth(1, 300)
        self.doctorMainTable.setColumnWidth(2, 70)
        self.doctorMainTable.setColumnWidth(3, 70)
        self.doctorMainTable.setColumnWidth(4, 70)
        self.doctorMainTable.setColumnWidth(5, 190)
        self.doctorMainTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.doctorMainTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.doctorMainTable.verticalHeader().setVisible(False)
        self.doctorMainTable.cellClicked.connect(self.viewPrescription)
        self.logoutButton.clicked.connect(self.logoutApp)
        # self.viewButton.clicked.connect(self.viewPrescription)
        self.showRecords()

    def showRecords(self):
        retrieveRecordsController = C.RetrieveRecordsController()
        listOfRecords = retrieveRecordsController.retrieveUserPrescriptions(UserNo)
        for rowNo, rowRecords in enumerate(listOfRecords):
            self.doctorMainTable.insertRow(rowNo)
            for colNo, record in enumerate(rowRecords):
                self.doctorMainTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))

    def viewPrescription(self):
        row = self.doctorMainTable.currentRow()
        global StringCode
        StringCode = self.doctorMainTable.item(row, 1).text()
        toViewPrescription = DoctorViewPrescription()
        widget.addWidget(toViewPrescription)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def logoutApp(self):
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Logout")
        msgbox.setText("Logging out")
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()
        # calling LoginView() of boundary class
        RetToLogin = LoginView()
        widget.addWidget(RetToLogin)
        widget.setCurrentIndex(widget.currentIndex()+1)


class DoctorViewPrescription(QDialog):
    def __init__(self):
        super(DoctorViewPrescription, self).__init__()
        loadUi("doctorViewPrescription.ui", self)
        widget.setFixedSize(730, 650)
        self.doctorViewPresTable.setColumnWidth(0, 200)
        self.doctorViewPresTable.setColumnWidth(1, 90)
        self.doctorViewPresTable.setColumnWidth(2, 321)
        self.backButton.clicked.connect(self.toHome)
        self.doctorViewPresTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.doctorViewPresTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.doctorViewPresTable.verticalHeader().setVisible(False)
        self.displayDetails()

    def displayDetails(self):
        print("string Code passed: ", StringCode)
        Retrieve1RecordControl = C.Retrieve1RecordController()
        listofdetails, listofmeds = Retrieve1RecordControl.retrieveRecord(StringCode)
        self.PrescriptionIdLine.setText(str(listofdetails[0]))
        self.patientIdLine.setText(str(listofdetails[1]))
        self.doctorIdLine.setText(str(listofdetails[2]))
        self.prescriptionDateLine.setText(str(listofdetails[3]))
        self.statusMenu.currentText()
        for rowNo, rowRecords in enumerate(listofmeds):
            self.doctorViewPresTable.insertRow(rowNo)
            for colNo, record in enumerate(rowRecords):
                self.doctorViewPresTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))

    def toHome(self):
        toHome = DoctorHome()
        widget.addWidget(toHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class PharmacistHome(QMainWindow):
    def __init__(self):
        super(PharmacistHome, self).__init__()
        loadUi("pharmacistMainWindow.ui", self)
        widget.setFixedSize(930, 750)
        self.pharmacistMainTable.setColumnWidth(0, 100)
        self.pharmacistMainTable.setColumnWidth(1, 300)
        self.pharmacistMainTable.setColumnWidth(2, 70)
        self.pharmacistMainTable.setColumnWidth(3, 70)
        self.pharmacistMainTable.setColumnWidth(4, 70)
        self.pharmacistMainTable.setColumnWidth(5, 190)
        self.pharmacistMainTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.pharmacistMainTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.pharmacistMainTable.verticalHeader().setVisible(False)
        self.pharmacistMainTable.cellClicked.connect(self.viewPrescription)
        self.logoutButton.clicked.connect(self.logoutApp)
        self.showRecords()

    def showRecords(self):
        retrieveRecordsController = C.RetrieveRecordsController()
        listOfRecords = retrieveRecordsController.retrieveUserPrescriptions(UserNo)
        for rowNo, rowRecords in enumerate(listOfRecords):
            self.pharmacistMainTable.insertRow(rowNo)
            for colNo, record in enumerate(rowRecords):
                self.pharmacistMainTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))

    def viewPrescription(self):
        row = self.pharmacistMainTable.currentRow()
        global StringCode
        StringCode = self.pharmacistMainTable.item(row, 1).text()
        toViewPrescription = PharmacistViewPrescription()
        widget.addWidget(toViewPrescription)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def logoutApp(self):
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Logout")
        msgbox.setText("Logging out")
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()
        RetToLogin = LoginView()
        widget.addWidget(RetToLogin)
        widget.setCurrentIndex(widget.currentIndex()+1)


class PharmacistViewPrescription(QDialog):
    def __init__(self):
        super(PharmacistViewPrescription, self).__init__()
        loadUi("pharmacistViewPrescription.ui", self)
        widget.setFixedSize(730, 650)
        self.pharmacistViewPresTable.setColumnWidth(0, 200)
        self.pharmacistViewPresTable.setColumnWidth(1, 90)
        self.pharmacistViewPresTable.setColumnWidth(2, 321)
        self.backButton.clicked.connect(self.toHome)
        self.pharmacistViewPresTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.pharmacistViewPresTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.pharmacistViewPresTable.verticalHeader().setVisible(False)
        self.displayDetails()

    def displayDetails(self):
        print("string Code passed: ", StringCode)
        Retrieve1RecordControl = C.Retrieve1RecordController()
        listofdetails, listofmeds = Retrieve1RecordControl.retrieveRecord(StringCode)
        self.PrescriptionIdLine.setText(str(listofdetails[0]))
        self.patientIdLine.setText(str(listofdetails[1]))
        self.doctorIdLine.setText(str(listofdetails[2]))
        self.prescriptionDateLine.setText(str(listofdetails[3]))
        self.statusMenu.currentText()
        for rowNo, rowRecords in enumerate(listofmeds):
            self.pharmacistViewPresTable.insertRow(rowNo)
            for colNo, record in enumerate(rowRecords):
                self.pharmacistViewPresTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))

    def toHome(self):
        toHome = PharmacistHome()
        widget.addWidget(toHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)

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


class AdminHome(QMainWindow):
    def __init__(self):
        super(AdminHome, self).__init__()
        loadUi("adminMainWindow.ui", self)
        widget.setFixedSize(740, 790)
        widget.setWindowTitle("Admin Homepage")
        self.adminMainTable.setColumnWidth(0, 50)
        self.adminMainTable.setColumnWidth(1, 100)
        self.adminMainTable.setColumnWidth(2, 100)
        self.adminMainTable.setColumnWidth(3, 150)
        self.adminMainTable.setColumnWidth(4, 100)
        self.adminMainTable.setColumnWidth(4, 100)
        self.adminMainTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.adminMainTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.adminMainTable.verticalHeader().setVisible(False)
        self.adminMainTable.cellClicked.connect(self.viewUserInfo)
        self.logoutButton.clicked.connect(self.logoutApp)
        self.showUserRecords()

    def showUserRecords(self):      # to show list of users on admin homepage
        retrieveUsersControl = C.RetrieveUserInfoController()
        # boundary calling controller
        listOfRecords = retrieveUsersControl.retrieveUserInfo(UserNo)
        for rowNo, rowRecords in enumerate(listOfRecords):
            self.adminMainTable.insertRow(rowNo)
            for colNo, record in enumerate(rowRecords):
                self.adminMainTable.setItem(rowNo, colNo, QTableWidgetItem(str(record)))

    def viewUserInfo(self):
        row = self.adminMainTable.currentRow()
        global UserNo
        UserNo = self.adminMainTable.item(row, 0).text()
        toViewUserInfo = AdminViewUserInfo()
        widget.addWidget(toViewUserInfo)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def logoutApp(self):
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Logout")
        msgbox.setText("Logging out")
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.exec_()
        RetToLogin = LoginView()
        widget.addWidget(RetToLogin)
        widget.setCurrentIndex(widget.currentIndex()+1)


class AdminViewUserInfo(QDialog):
    def __init__(self):
        super(AdminViewUserInfo, self).__init__()
        loadUi("adminEditUser.ui", self)
        widget.setFixedSize(730, 650)
        self.backButton.clicked.connect(self.toHome)
        self.displayDetails()

    def displayDetails(self):
        print("User No passed: ", UserNo)
        Retrieve1UserControl = C.RetrieveSpecificUserController()
        listofdetails = Retrieve1UserControl.retrieveSpecificUserInfo(UserNo)
        self.userMenu.currentText()
        self.idLine.setText(str(listofdetails[0]))
        self.nameLine.setText(str(listofdetails[1]))
        self.emailLine.setText(str(listofdetails[2]))
        self.addressLine.setText(str(listofdetails[3]))
        self.telLine.setText(str(listofdetails[4]))

    def toHome(self):
        toHome = AdminHome()
        widget.addWidget(toHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = LoginView()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(600)
    widget.setFixedHeight(530)
    widget.show()
    app.exec()