import sys, res, controller
from sqlite3 import IntegrityError

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QMessageBox, QTableWidgetItem,QAbstractItemView
from PyQt5.uic import loadUi
import controller as C

status_dict = {
    'Not Collected': 0,
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
        loadUi("loginDialog.ui", self)                          # load the ui file
        self.loginButton.clicked.connect(self.login)            # loginButton
        self.registerButton.clicked.connect(self.go_to_create)  # registerButton

    def login(self):
        email = self.email.text()           # get email from user input
        password = self.password.text()     # get password from user input
        usertype = self.userMenu.currentText()

        # boundary calling controller
        user = C.UserController.login(email, password)
        if user:   # if input valid
            C.Session.set_user(user)
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Login success")
            msgbox.setText("WELCOME TO GD PRESCRIPTION")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()
            print(f'logged in {user}')
            if user.role == "Doctor":
                doctor_home = DoctorHome()
                widget.addWidget(doctor_home)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif user.role == "Patient":
                patient_home = PatientHome()
                widget.addWidget(patient_home)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif user.role == "Pharmacist":
                pharmacist_home = PharmacistHome()
                widget.addWidget(pharmacist_home)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif user.role == 'Admin':
                admin_home = AdminHome()
                widget.addWidget(admin_home)
                widget.setCurrentIndex(widget.currentIndex() + 1)
        else:   # if input invalid
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Login fail")
            msgbox.setText("INVALID CREDENTIALS INPUT!")
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()

    def go_to_create(self):
        registerAcc = Register()
        widget.addWidget(registerAcc)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Home(QMainWindow):
    user_controller = C.UserController()
    prescription_controller = C.PrescriptionController()

    def __init__(self, window, column_sizes=None):
        super(Home, self).__init__()
        if column_sizes is None:
            column_sizes = [100, 100, 200, 200, 180]
        loadUi(window, self)
        widget.setFixedSize(930,750)
        for i in range(len(column_sizes)):
            self.table.setColumnWidth(i, column_sizes[i])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.logoutButton.clicked.connect(self.logout_app)
        self.get_records()

    def display_records(self, records):
        if records:
            self.table.setRowCount(len(records))
            for count, item in enumerate(records):
                doctor_name = self.user_controller.retrieve_user(item.doctor_id).name
                patient_name = self.user_controller.retrieve_user(item.patient_id).name
                self.table.setItem(count, 0, QTableWidgetItem(str(item.object_id)))
                self.table.setItem(count, 1, QTableWidgetItem(str(item.date_created)))
                self.table.setItem(count, 2, QTableWidgetItem(str(doctor_name)))
                self.table.setItem(count, 3, QTableWidgetItem(str(patient_name)))
                self.table.setItem(count, 4, QTableWidgetItem(str(item.get_status_string())))

    def display_users(self, users):
        if users:
            self.table.setRowCount(len(users))
            for count, user in enumerate(users):
                self.table.setItem(count, 0, QTableWidgetItem(str(user.object_id)))
                self.table.setItem(count, 1, QTableWidgetItem(str(user.name)))
                self.table.setItem(count, 2, QTableWidgetItem(str(user.email)))
                self.table.setItem(count, 3, QTableWidgetItem(str(user.address)))
                self.table.setItem(count, 4, QTableWidgetItem(str(user.phone_number)))
                self.table.setItem(count, 5, QTableWidgetItem(str(user.role)))

    def view_prescription(self):
        row = self.table.currentRow()
        print('view_prescription called')
        C.Session.set_context(C.PrescriptionController.retrieve_prescription(self.table.item(row, 0).text()))

    def view_user(self):
        row = self.table.currentRow()
        print('view_user called')
        print(self.table.item(row, 0).text())
        C.Session.set_context(C.UserController.retrieve_user(self.table.item(row, 0).text()))
        print(C.Session.get_context())

    def logout_app(self):
        # calling LoginView() of boundary class
        C.Session.set_user(None)
        ret_to_login = LoginView()
        widget.addWidget(ret_to_login)
        widget.setCurrentIndex(widget.currentIndex()+1)


class PatientHome(Home):
    def __init__(self):
        super(PatientHome, self).__init__('patientMainWindow.ui')
        self.table.cellClicked.connect(self.view_prescription)
        
    def get_records(self):
        print(f'Session user: {C.Session.get_user()}')
        session_user = C.Session.get_user()
        self.idLine.setText(str(session_user.object_id))
        self.nameLine.setText(session_user.name)
        self.emailLine.setText(session_user.email)
        self.addressLine.setText(session_user.address)
        self.telLine.setText(session_user.phone_number)
        self.display_records(self.prescription_controller.retrieve_patient_prescriptions(session_user.object_id))

    def view_prescription(self):
        super(PatientHome, self).view_prescription()
        prescription = PatientViewPrescription()
        widget.addWidget(prescription)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DoctorHome(Home):
    def __init__(self):
        super(DoctorHome, self).__init__('doctorMainWindow.ui')
        self.table.cellClicked.connect(self.view_prescription)
    
    def get_records(self):
        # boundary calling controller
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
        self.table.cellClicked.connect(self.view_prescription)
    
    def get_records(self):
        # boundary calling controller
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
        
    def get_records(self):
        users = self.user_controller.retrieve_all_users()
        self.display_users(users)

    def view_user(self):
        super(AdminHome, self).view_user()
        view_user_info = AdminViewUser()
        widget.addWidget(view_user_info)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ViewPrescription(QDialog):
    user_controller = C.UserController()

    def __init__(self, window, widget_size=None, column_sizes=None):
        super(ViewPrescription, self).__init__()
        if widget_size is None:
            widget_size = [730, 650]
        if column_sizes is None:
            column_sizes = [100, 400, 100]
        loadUi(window, self)
        widget.setFixedSize(widget_size[0], widget_size[1])
        for i in range(len(column_sizes)):
            self.table.setColumnWidth(i, column_sizes[i])
        self.backButton.clicked.connect(self.to_home)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.get_records()

    def get_records(self):
        prescription = C.Session.get_context()
        print(prescription)
        doctor_name = self.user_controller.retrieve_user(prescription.doctor_id).name
        patient_name = self.user_controller.retrieve_user(prescription.patient_id).name
        self.PrescriptionIdLine.setText(str(prescription.object_id))
        self.patientIdLine.setText(str(patient_name))
        self.doctorIdLine.setText(str(doctor_name))
        self.prescriptionDateLine.setText(prescription.date_created)
        self.statusMenu.setCurrentIndex(status_dict[prescription.get_status_string()])
        self.display_records(C.MedicineQuantityController.retrieve_prescription_medicines(prescription.object_id))

    def display_records(self, records):
        if records:
            self.table.setRowCount(len(records))
            for count, item in enumerate(records):
                medicine_name = C.MedicineController.retrieve_medicine(item.object_id).name
                self.table.setItem(count, 0, QTableWidgetItem(str(item.object_id)))
                self.table.setItem(count, 1, QTableWidgetItem(str(medicine_name)))
                self.table.setItem(count, 2, QTableWidgetItem(str(item.quantity)))


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
    user_controller = C.UserController

    def __init__(self, window):
        super(ViewUser, self).__init__()
        loadUi(window, self)
        widget.setFixedSize(730, 650)
        self.backButton.clicked.connect(self.to_home)
        self.display_details()

    def display_details(self):
        context_user = C.Session.get_context()
        print(f'{context_user = }')
        self.userMenu.setCurrentIndex(role_dict[context_user.role])
        self.idLine.setText(str(context_user.object_id))
        self.nameLine.setText(context_user.name)
        self.emailLine.setText(context_user.email)
        self.addressLine.setText(context_user.address)
        self.telLine.setText(context_user.phone_number)


class AdminViewUser(ViewUser):
    def __init__(self):
        super(AdminViewUser, self).__init__('adminEditUser.ui')
        self.saveButton.clicked.connect(self.save_user)

    def to_home(self):
        home = AdminHome()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def save_user(self):
        print('saving user...')
        user_id = self.idLine.text()
        role = self.userMenu.currentText()
        name = self.nameLine.text()
        email = self.emailLine.text()
        address = self.addressLine.text()
        phone_number = self.telLine.text()
        print(f'{user_id = }')
        print(f'{role = }')
        print(f'{name = }')
        print(f'{email = }')
        print(f'{address = }')
        print(f'{phone_number = }')
        try:
            self.user_controller.save_user(user_id, email, name, phone_number, address, role)
        except IntegrityError as err:
            print(f'{err}')         # ERROR MESSAGE SHOW ON SCREEN


class Register(QDialog):
    def __init__(self):
        super(Register, self).__init__()
        loadUi("registerDialog.ui", self)
        self.registerButton.clicked.connect(self.register)
        self.loginButton.clicked.connect(self.go_to_login)

    def register(self):
        email = self.email.text()
        if self.password.text() == self.confirmPass.text():
            password = self.password.text()
        print("Successfully registering in with email: ", email, "and password: ", password)
        self.go_to_login()

    def go_to_login(self):
        login = LoginView()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = LoginView()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(600)
    widget.setFixedHeight(530)
    widget.show()
    app.exec()
