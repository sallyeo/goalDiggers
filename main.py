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
        # Call to controller
        roles = C.UserTypeController().retrieve_all_roles()
        for role in roles:
            self.userMenu.addItem(role.role)

    def login(self):
        email = self.email.text()           # get email from user input
        password = self.password.text()     # get password from user input
        usertype = self.userMenu.currentText()

        # boundary calling controller
        user = C.UserController.login(email, password)
        if user:   # if input valid
            C.Session.set_user(user)
            # msgbox = QMessageBox()
            # msgbox.setWindowTitle("Login success")
            # msgbox.setText("WELCOME TO GD PRESCRIPTION")
            # msgbox.setStandardButtons(QMessageBox.Ok)
            # msgbox.exec_()
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
            column_sizes = [50, 100, 100, 150, 100, 100]
        loadUi(window, self)
        widget.setFixedSize(930,750)
        for i in range(len(column_sizes)):
            self.table.setColumnWidth(i, column_sizes[i])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        # self.table.verticalHeader().setVisible(False)
        self.logoutButton.clicked.connect(self.logout_app)
        self.get_records()

    def get_records(self):
        pass

    def display_details(self):
        pass

    def display_prescriptions(self, records):
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
        C.Session.set_context('prescription', C.PrescriptionController.retrieve_prescription(self.table.item(row, 0).text()))

    def view_user(self):
        row = self.table.currentRow()
        C.Session.set_context('user', C.UserController.retrieve_user(self.table.item(row, 0).text()))

    @staticmethod
    def load_page(page):
        widget.addWidget(page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def logout_app(self):
        # calling LoginView() of boundary class
        C.Session.set_user(None)
        self.load_page(LoginView())


class PatientHome(Home):
    def __init__(self):
        super(PatientHome, self).__init__('patientMainWindow.ui', [100, 100, 200, 200, 180])
        self.table.cellClicked.connect(self.view_prescription)
        
    def get_records(self):
        print(f'Session user: {C.Session.get_user()}')
        session_user = C.Session.get_user()
        self.display_details()
        self.display_prescriptions(self.prescription_controller.retrieve_patient_prescriptions(session_user.object_id))

    def display_details(self):
        session_user = C.Session.get_user()
        self.idLine.setText(str(session_user.object_id))
        self.nameLine.setText(session_user.name)
        self.emailLine.setText(session_user.email)
        self.addressLine.setText(session_user.address)
        self.telLine.setText(session_user.phone_number)

    def view_prescription(self):
        super(PatientHome, self).view_prescription()
        self.load_page(PatientViewPrescription())


class DoctorHome(Home):
    def __init__(self):
        super(DoctorHome, self).__init__('doctorMainWindow.ui')
        # self.table.cellClicked.connect(self.view_prescription)
        self.table.cellClicked.connect(self.view_user)
    
    def get_records(self):
        # boundary calling controller
        users = C.UserController.retrieve_users_by_role('Patient')
        self.display_users(users)
        # prescriptions = C.PrescriptionController.retrieve_all_prescriptions()
        # self.display_records(prescriptions)

    # def view_prescription(self):
    #     super(DoctorHome, self).view_prescription()
    #     prescription = DoctorViewPrescription()
    #     widget.addWidget(prescription)
    #     widget.setCurrentIndex(widget.currentIndex() + 1)

    def view_user(self):
        super(DoctorHome, self).view_user()
        self.load_page(DoctorViewPatient())


class PharmacistHome(Home):
    def __init__(self):
        super(PharmacistHome, self).__init__('pharmacistMainWindow.ui')
        # self.table.cellClicked.connect(self.view_prescription)
        self.table.cellClicked.connect(self.view_user)

    def get_records(self):
        # boundary calling controller
        users = C.UserController.retrieve_users_by_role('Patient')
        self.display_users(users)
        # prescriptions = C.PrescriptionController.retrieve_all_prescriptions()
        # self.display_records(prescriptions)

    def view_user(self):
        super(PharmacistHome, self).view_user()
        self.load_page(PharmacistViewPatient())

    # def view_prescription(self):
    #     super(PharmacistHome, self).view_prescription()
    #     prescription = PharmacistViewPrescription()
    #     widget.addWidget(prescription)
    #     widget.setCurrentIndex(widget.currentIndex() + 1)


class AdminHome(Home):
    def __init__(self):
        super(AdminHome, self).__init__('adminMainWindow.ui')
        self.table.cellClicked.connect(self.view_user)
        self.addUserButton.clicked.connect(self.create_user)
        
    def get_records(self):
        users = self.user_controller.retrieve_all_users()
        self.display_users(users)

    def view_user(self):
        super(AdminHome, self).view_user()
        self.load_page(AdminViewUser())

    def create_user(self):
        self.load_page(AdminCreateUser())


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
        self.backButton.clicked.connect(self.go_back)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        # self.table.verticalHeader().setVisible(False)
        self.get_records()

    def get_records(self):
        prescription = C.Session.get_context('prescription')
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
        self.table.setRowCount(0)
        if records:
            self.table.setRowCount(len(records))
            for count, item in enumerate(records):
                medicine_name = C.MedicineController.retrieve_by_id(item.medicine_id).name
                self.table.setItem(count, 0, QTableWidgetItem(str(item.object_id)))
                self.table.setItem(count, 1, QTableWidgetItem(str(medicine_name)))
                self.table.setItem(count, 2, QTableWidgetItem(str(item.quantity)))

    def go_home(self):
        pass

    def load_page(self, page):
        widget.addWidget(page)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class PatientViewPrescription(ViewPrescription):
    def __init__(self):
        super(PatientViewPrescription, self).__init__('patientViewPrescription.ui')

    def go_back(self):
        self.load_page(PatientHome())


class DoctorViewPrescription(ViewPrescription):
    def __init__(self):
        super(DoctorViewPrescription, self).__init__('doctorViewPrescription.ui')
        self.table.cellClicked.connect(self.edit_prescription)

    def go_back(self):
        self.load_page(DoctorViewPatient())

    def edit_prescription(self):
        row = self.table.currentRow()
        C.Session.set_context('medicine_quantity', C.MedicineQuantityController.retrieve_by_id(self.table.item(row, 0).text()))
        self.load_page(DoctorEditMedicine(DoctorViewPrescription()))


class PharmacistViewPrescription(ViewPrescription):
    def __init__(self):
        super(PharmacistViewPrescription, self).__init__('pharmacistViewPrescription.ui')

    def go_back(self):
        self.load_page(PharmacistViewPatient())


class ViewUser(QDialog):
    user_controller = C.UserController
    prescription_controller = C.PrescriptionController

    def __init__(self, window):
        super(ViewUser, self).__init__()
        loadUi(window, self)
        widget.setFixedSize(730, 650)

    def get_records(self):
        pass

    def display_details(self):
        pass

    def load_page(self, page):
        widget.addWidget(page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def display_prescriptions(self, records):
        print(f'{records = }')
        if records:
            self.table.setRowCount(len(records))
            for count, item in enumerate(records):
                doctor_name = self.user_controller.retrieve_user(item.doctor_id).name
                pharmacist = self.user_controller.retrieve_user(item.pharmacist_id)
                pharmacist_name = pharmacist.name if pharmacist else ''
                self.table.setItem(count, 0, QTableWidgetItem(str(item.object_id)))
                self.table.setItem(count, 1, QTableWidgetItem(str(item.date_created)))
                self.table.setItem(count, 2, QTableWidgetItem(str(doctor_name)))
                self.table.setItem(count, 3, QTableWidgetItem(str(pharmacist_name) or ''))
                self.table.setItem(count, 4, QTableWidgetItem(str(item.get_status_string())))

    def view_prescription(self):
        row = self.table.currentRow()
        C.Session.set_context('prescription', C.PrescriptionController.retrieve_prescription(self.table.item(row, 0).text()))


class AdminViewUser(ViewUser):
    def __init__(self):
        super(AdminViewUser, self).__init__('adminEditUser.ui')
        self.saveButton.clicked.connect(self.save_user)
        roles = C.UserTypeController().retrieve_all_roles()
        for role in roles:
            self.userMenu.addItem(role.role)
        self.backButton.clicked.connect(self.go_back)
        self.display_details()

    def go_back(self):
        self.load_page(AdminHome())

    def save_user(self):
        print('saving user...')
        user_id = self.idLine.text()
        role = self.userMenu.currentText()
        name = self.nameLine.text()
        email = self.emailLine.text()
        address = self.addressLine.text()
        phone_number = self.telLine.text()
        try:
            self.user_controller.save_user(user_id, email, name, phone_number, address, role)
        except IntegrityError as err:
            print(f'{err}')         # ERROR MESSAGE SHOW ON SCREEN
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Login fail")
            msgbox.setText(err)
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.exec_()

    def display_details(self):
        context_user = C.Session.get_context('user')
        print(f'{context_user = }')
        self.userMenu.setCurrentIndex(role_dict[context_user.role])
        self.idLine.setText(str(context_user.object_id))
        self.nameLine.setText(context_user.name)
        self.emailLine.setText(context_user.email)
        self.addressLine.setText(context_user.address)
        self.telLine.setText(context_user.phone_number)


class DoctorViewPatient(ViewUser):
    def __init__(self, column_sizes=None):
        super(DoctorViewPatient, self).__init__('doctorViewPatient.ui')
        widget.setFixedSize(730, 650)
        # self.table.verticalHeader().setVisible(False)   # remove most left column
        if column_sizes is None:
            column_sizes = [50, 100, 100, 100, 100]
        for i in range(len(column_sizes)):
            self.table.setColumnWidth(i, column_sizes[i])
        self.backButton.clicked.connect(self.go_back)
        self.addPrescriptionButton.clicked.connect(self.add_prescription)
        self.table.cellClicked.connect(self.view_prescription)
        self.get_records()

    def go_back(self):
        self.load_page(DoctorHome())

    def get_records(self):
        context_user = C.Session.get_context('user')
        self.display_details()
        self.display_prescriptions(self.prescription_controller.retrieve_patient_prescriptions(context_user.object_id))

    def display_details(self):
        context_user = C.Session.get_context('user')
        self.nameLine.setText(context_user.name)
        self.emailLine.setText(context_user.email)
        self.phoneNumberLine.setText(context_user.phone_number)

    def view_prescription(self):
        super(DoctorViewPatient, self).view_prescription()
        self.load_page(DoctorViewPrescription())

    def add_prescription(self):
        # C.Session.set_context('cart', C.CartController.retrieve_cart_by_patient(C.Session.get_context('user').object_id))
        self.load_page(DoctorAddPrescription())


class PharmacistViewPatient(ViewUser):
    def __init__(self, column_sizes=None):
        super(PharmacistViewPatient, self).__init__('pharmacistViewPatient.ui')
        if column_sizes is None:
            column_sizes = [100, 100, 100, 100, 100]
        for i in range(len(column_sizes)):
            self.table.setColumnWidth(i, column_sizes[i])
            self.backButton.clicked.connect(self.go_back)
            self.table.cellClicked.connect(self.view_prescription)
            self.get_records()

    def go_back(self):
        self.load_page(PharmacistHome())

    def get_records(self):
        context_user = C.Session.get_context('user')
        self.display_details()
        self.display_prescriptions(self.prescription_controller.retrieve_patient_prescriptions(context_user.object_id))

    def display_details(self):
        context_user = C.Session.get_context('user')
        self.nameLine.setText(context_user.name)
        self.emailLine.setText(context_user.email)
        self.phoneNumberLine.setText(context_user.phone_number)

    def view_prescription(self):
        super(PharmacistViewPatient, self).view_prescription()
        self.load_page(PharmacistViewPrescription())


class AdminCreateUser(QDialog):
    user_controller = C.UserController

    def __init__(self):
        super(AdminCreateUser, self).__init__()
        loadUi('adminCreateUser.ui', self)
        self.createButton.clicked.connect(self.create_user)
        self.backButton.clicked.connect(self.go_back)
        roles = C.UserTypeController().retrieve_all_roles()
        for role in roles:
            self.userMenu.addItem(role.role)

    def go_back(self):
        self.load_page(AdminHome())

    def load_page(self, home):
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def create_user(self):
        role = self.userMenu.currentText()
        name = self.nameLine.text()
        email = self.emailLine.text()
        address = self.addressLine.text()
        phone_number = self.telLine.text()
        password1 = self.password1Line.text()
        password2 = self.password2Line.text()
        if password1 != password2:
            self.errorLabel.setText('Passwords do not match.')
            return
        try:
            self.user_controller.create_user(email, name, phone_number, address, role, password1)
            self.success('User created')
        except ValueError as err:
            print(err)

    def success(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Success !')
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        self.go_back()


class DoctorAddPrescription(QDialog):
    user_controller = C.UserController
    prescription_controller = C.PrescriptionController
    medicine_controller = C.MedicineController
    medicine_quantity_controller = C.MedicineQuantityController

    def __init__(self):
        super(DoctorAddPrescription, self).__init__()
        loadUi('doctorAddPrescription.ui', self)
        widget.setFixedSize(730, 650)
        self.backButton.clicked.connect(self.go_back)
        self.prescribeButton.clicked.connect(self.prescribe)
        self.addButton.clicked.connect(self.add_medicine)
        self.patientNameLine.setText(str(C.Session.get_context('user').name))
        self.table.cellClicked.connect(self.edit_medicine)
        medicines = self.medicine_controller.retrieve_all_medicines()
        for medicine in medicines:
            self.medMenu.addItem(medicine.name)
        self.get_and_display_records()

    def get_and_display_records(self):
        cart = C.CartController.retrieve_cart_by_patient(C.Session.get_context('user').object_id)
        print(f'{cart = }')
        medicine_quantities = C.MedicineQuantityController.retrieve_cart_medicines(cart.object_id)
        print(f'Doctor add prescription page: {medicine_quantities = }')
        if medicine_quantities:
            self.table.setRowCount(len(medicine_quantities))
            for count, item in enumerate(medicine_quantities):
                medicine_name = C.MedicineController.retrieve_by_id(item.medicine_id).name
                self.table.setItem(count, 0, QTableWidgetItem(str(item.object_id)))
                self.table.setItem(count, 1, QTableWidgetItem(str(medicine_name)))
                self.table.setItem(count, 2, QTableWidgetItem(str(item.quantity)))

    def go_back(self):
        widget.addWidget(DoctorViewPatient())
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def prescribe(self):
        cart = C.CartController.retrieve_cart_by_patient(C.Session.get_context('user').object_id)
        C.CartController.prescribe_medicines(cart.object_id)
        self.refresh_table()

    def add_medicine(self):
        try:
            selected_medicine = str(self.medMenu.currentText())
            selected_quantity = int(self.quantityMenu.currentText())
            print(f'Add {selected_quantity} {selected_medicine}')
            self.medicine_quantity_controller.add_new(selected_quantity, selected_medicine, C.Session.get_context('user').object_id)
            self.refresh_table()
        except ValueError as err:
            print('Quantity must be a integer !')

    def refresh_table(self):
        self.table.setRowCount(0)
        self.get_and_display_records()

    def edit_medicine(self):
        row = self.table.currentRow()
        print(self.table.item(row, 0).text())
        medicine_quantity = C.MedicineQuantityController.retrieve_by_id(self.table.item(row, 0).text())
        print(f'{medicine_quantity = }')
        C.Session.set_context('medicine_quantity', medicine_quantity)
        self.load_page(DoctorEditMedicine(DoctorAddPrescription()))

    @staticmethod
    def load_page(page):
        widget.addWidget(page)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DoctorEditMedicine(QDialog):
    def __init__(self, from_page):
        super(DoctorEditMedicine, self).__init__()
        self.back_page = from_page
        loadUi('doctorEditMedicine.ui', self)
        widget.setFixedSize(930, 750)
        self.saveButton.clicked.connect(self.save_medicine)
        self.deleteButton.clicked.connect(self.delete)
        self.backButton.clicked.connect(self.go_back)
        self.display_details()

    def display_details(self):
        medicine_quantity = C.Session.get_context('medicine_quantity')
        medicines = C.MedicineController.retrieve_all_medicines()
        for medicine in medicines:
            self.medMenu.addItem(medicine.name)
        medicine_name = C.MedicineController.retrieve_by_id(medicine_quantity.medicine_id).name
        index = self.medMenu.findText(medicine_name)
        if index >= 0:
            self.medMenu.setCurrentIndex(index)
        self.quantityLine.setText(str(medicine_quantity.quantity))

    def save_medicine(self):
        medicine_quantity = C.Session.get_context('medicine_quantity')
        medicine_id = C.MedicineController.retrieve_by_name(self.medMenu.currentText()).object_id
        medicine_quantity.medicine_id = medicine_id
        medicine_quantity.quantity = int(self.quantityLine.text())
        print(f'{medicine_quantity.object_id = }')
        print(f'{medicine_quantity.medicine_id = }')
        print(f'{medicine_quantity.quantity = }')
        C.MedicineQuantityController.save_medicine_quantity(
            medicine_quantity.object_id,
            medicine_quantity.prescription_id,
            medicine_quantity.cart_id,
            medicine_quantity.medicine_id,
            medicine_quantity.quantity,
        )
        self.go_back()

    def delete(self):
        C.MedicineQuantityController.delete(C.Session.get_context('medicine_quantity').object_id)
        self.go_back()

    def go_back(self):
        # self.load_page(DoctorAddPrescription())
        self.load_page(self.back_page)

    @staticmethod
    def load_page(page):
        widget.addWidget(page)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Register(QDialog):
    def __init__(self):
        super(Register, self).__init__()
        loadUi("registerDialog.ui", self)
        self.registerButton.clicked.connect(self.register)
        self.loginButton.clicked.connect(self.go_login)

    def register(self):
        email = self.email.text()
        if self.password.text() == self.confirmPass.text():
            password = self.password.text()
        print("Successfully registering in with email: ", email, "and password: ", password)
        self.go_login()

    def go_login(self):
        login = LoginView()
        widget.addWidget(login)
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
