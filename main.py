import sys
import res        # Res for images
from sqlite3 import IntegrityError
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QAbstractItemView
from PyQt5.uic import loadUi
import controller as C


class LoginView(QDialog):
    def __init__(self):
        super(LoginView, self).__init__()
        loadUi("loginDialog.ui", self)                          # load the ui file
        self.loginButton.clicked.connect(self.login)            # loginButton
        self.registerButton.clicked.connect(self.register)      # registerButton
        self.email.returnPressed.connect(self.login)            # Return key pressed
        self.password.returnPressed.connect(self.login)         # Return key pressed

    def login(self):
        email = self.email.text()           # get email from user input
        password = self.password.text()     # get password from user input

        # boundary calling controller
        if user := C.UserController.login(email, password):      # if input valid
            C.Session.set_user(user)
            print(f'logged in as {user}')
            if user.role == "Doctor":
                self.go_to(DoctorHome())
            elif user.role == "Patient":
                self.go_to(PatientHome())
            elif user.role == "Pharmacist":
                self.go_to(PharmacistHome())
            elif user.role == 'Admin':
                self.go_to(AdminHome())
        else:       # if input invalid
            self.show_message('Login failed', 'Invalid credentials')

    def register(self):
        self.go_to(Register())

    def go_to(self, page):
        widget.addWidget(page)
        widget.setCurrentIndex(widget.currentIndex()+1)

    @staticmethod
    def show_message(title, text):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


class Home(QMainWindow):
    user_controller = C.UserController()
    prescription_controller = C.PrescriptionController()

    def __init__(self, window, column_sizes=None):
        super(Home, self).__init__()
        if column_sizes is None:
            column_sizes = [50, 130, 210, 140, 90, 90]
        loadUi(window, self)
        widget.setFixedSize(930, 750)
        for i in range(len(column_sizes)):
            self.table.setColumnWidth(i, column_sizes[i])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.searchButton.clicked.connect(self.search)
        self.searchBarLine.returnPressed.connect(self.search)
        self.logoutButton.clicked.connect(self.logout_app)
        self.get_records()

    def get_records(self):
        pass

    def display_details(self):
        pass

    def search(self):
        pass

    def display_prescriptions(self, records):
        self.table.setRowCount(0)
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
        self.table.setRowCount(0)
        if users:
            print(f'{users = }')
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
        prescription = C.PrescriptionController.retrieve_prescription(self.table.item(row, 0).text())
        C.Session.set_context('prescription', prescription)

    def view_user(self):
        row = self.table.currentRow()
        user = C.UserController.retrieve_user(self.table.item(row, 0).text())
        C.Session.set_context('user', user)

    @staticmethod
    def load_page(page):
        widget.addWidget(page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def logout_app(self):
        C.Session.set_user(None)
        self.load_page(LoginView())


class PatientHome(Home):
    def __init__(self):
        super(PatientHome, self).__init__('patientMainWindow.ui', [110, 120, 165, 165, 120])
        widget.setFixedSize(820, 740)
        self.table.cellClicked.connect(self.view_prescription)
        
    def get_records(self):
        session_user = C.Session.get_user()
        self.display_details()
        self.display_prescriptions(self.prescription_controller.retrieve_patient_prescriptions(session_user.object_id))

    def display_prescriptions(self, records):
        self.table.setRowCount(0)
        if records:
            self.table.setRowCount(len(records))
            for count, item in enumerate(records):
                doctor_name = self.user_controller.retrieve_user(item.doctor_id).name
                pharmacist = self.user_controller.retrieve_user(item.pharmacist_id)
                pharmacist_name = pharmacist.name if pharmacist else ''
                self.table.setItem(count, 0, QTableWidgetItem(str(item.object_id)))
                self.table.setItem(count, 1, QTableWidgetItem(str(item.date_created)))
                self.table.setItem(count, 2, QTableWidgetItem(str(doctor_name)))
                self.table.setItem(count, 3, QTableWidgetItem(str(pharmacist_name)))
                self.table.setItem(count, 4, QTableWidgetItem(str(item.get_status_string())))

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

    def search(self):
        search_query = self.searchBarLine.text()
        user_prescriptions = []
        prescription = C.PrescriptionController.retrieve_prescription(search_query)
        if prescription and prescription.patient_id == C.Session.get_user().object_id:
            user_prescriptions.append(prescription)
        self.display_prescriptions(user_prescriptions) if user_prescriptions else self.get_records()


class DoctorHome(Home):
    def __init__(self):
        super(DoctorHome, self).__init__('doctorMainWindow.ui', [50, 150, 200, 250, 100])
        widget.setFixedSize(890, 750)
        self.table.cellClicked.connect(self.view_user)
    
    def get_records(self):
        users = C.UserController.retrieve_users_by_role('Patient')
        self.display_users(users)

    def view_user(self):
        super(DoctorHome, self).view_user()
        self.load_page(DoctorViewPatient())

    def search(self):
        result = []
        if search_query := self.searchBarLine.text():
            # if user:
            if user := C.UserController.retrieve_user(search_query):
                result = [user] if user.role == 'Patient' else []
        self.display_users(result) if result else self.get_records()


class PharmacistHome(Home):
    def __init__(self):
        super(PharmacistHome, self).__init__('pharmacistMainWindow.ui', [110, 120, 165, 165, 120])
        widget.setFixedSize(820, 740)
        self.table.cellClicked.connect(self.view_prescription)
        self.scanButton.clicked.connect(self.scan_code)

    def get_records(self):
        prescriptions = C.PrescriptionController.retrieve_all_prescriptions()
        self.display_prescriptions(prescriptions)

    def view_user(self):
        super(PharmacistHome, self).view_user()
        self.load_page(PharmacistViewPatient())

    def scan_code(self):
        code = C.QRController.read()
        prescription = C.PrescriptionController.retrieve_prescription(code)
        user = C.UserController.retrieve_user(prescription.patient_id)
        C.Session.set_context('prescription', prescription)
        C.Session.set_context('user', user)
        self.load_page(PharmacistViewPrescription())

    def view_prescription(self):
        super(PharmacistHome, self).view_prescription()
        self.load_page(PharmacistViewPrescription())

    def search(self):
        user_prescriptions = []
        if search_query := self.searchBarLine.text():
            if prescription := C.PrescriptionController.retrieve_prescription(search_query):
                user_prescriptions.append(prescription)
        print(f'{user_prescriptions = }')
        self.display_prescriptions(user_prescriptions) if user_prescriptions else self.get_records()


class AdminHome(Home):
    def __init__(self):
        super(AdminHome, self).__init__('adminMainWindow.ui')
        widget.setFixedSize(850, 720)
        self.table.cellClicked.connect(self.view_user)
        self.addUserButton.clicked.connect(self.create_user)
        self.addRoleButton.clicked.connect(self.add_role)
        self.searchRoleButton.clicked.connect(self.search_role)
        self.searchRoleLine.returnPressed.connect(self.search_role)

    def get_records(self):
        users = self.user_controller.retrieve_all_users()
        self.display_users(users)

    def view_user(self):
        super(AdminHome, self).view_user()
        self.load_page(AdminViewUser())

    def create_user(self):
        self.load_page(AdminCreateUser())

    def add_role(self):
        self.load_page(AdminAddRole())

    def search(self):
        all_search = []
        if search_query := self.searchBarLine.text():
            if user := C.UserController.retrieve_user(search_query):
                all_search.append(user)
        self.display_users(all_search) if all_search else self.get_records()

    def search_role(self):
        all_search = []
        if search_query := self.searchRoleLine.text():
            all_search = C.UserController.search_by_role(search_query)
        self.display_users(all_search) if all_search else self.get_records()


class ViewPrescription(QDialog):
    user_controller = C.UserController()

    def __init__(self, window, widget_size=None, column_sizes=None):
        super(ViewPrescription, self).__init__()
        if widget_size is None:
            widget_size = [730, 600]
        if column_sizes is None:
            column_sizes = [100, 100, 500]
        loadUi(window, self)
        widget.setFixedSize(widget_size[0], widget_size[1])
        for i in range(len(column_sizes)):
            self.table.setColumnWidth(i, column_sizes[i])
        self.backButton.clicked.connect(self.go_back)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.get_records()

    def get_records(self):
        prescription = C.Session.get_context('prescription')
        doctor_name = self.user_controller.retrieve_user(prescription.doctor_id).name
        patient_name = self.user_controller.retrieve_user(prescription.patient_id).name
        self.PrescriptionIdLine.setText(str(prescription.object_id))
        self.patientIdLine.setText(str(patient_name))
        self.doctorIdLine.setText(str(doctor_name))
        self.prescriptionDateLine.setText(prescription.date_created)
        index = self.statusMenu.findText(prescription.get_status_string())
        if index >= 0:
            self.statusMenu.setCurrentIndex(index)
        self.get_and_display_records()

    def get_and_display_records(self):
        self.table.setRowCount(0)
        prescription = C.Session.get_context('prescription')
        records = C.MedicineQuantityController.retrieve_prescription_medicines(prescription.object_id)
        self.table.setRowCount(0)
        if records:
            self.table.setRowCount(len(records))
            for count, item in enumerate(records):
                medicine_name = C.MedicineController.retrieve_by_id(item.medicine_id).name
                self.table.setItem(count, 0, QTableWidgetItem(str(item.object_id)))
                self.table.setItem(count, 1, QTableWidgetItem(str(item.quantity)))
                self.table.setItem(count, 2, QTableWidgetItem(str(medicine_name)))

    def go_home(self):
        pass

    def load_page(self, page):
        widget.addWidget(page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def refresh_table(self):
        self.table.setRowCount(0)
        self.get_and_display_records()


class PatientViewPrescription(ViewPrescription):
    def __init__(self):
        super(PatientViewPrescription, self).__init__('patientViewPrescription.ui')
        widget.setFixedSize(720, 600)
        self.table.setColumnHidden(0, True)

    def go_back(self):
        self.load_page(PatientHome())


class DoctorViewPrescription(ViewPrescription):
    def __init__(self):
        super(DoctorViewPrescription, self).__init__('doctorViewPrescription.ui')
        widget.setFixedSize(720, 700)
        self.table.cellClicked.connect(self.edit_prescription)
        self.table.setColumnHidden(0, True)
        self.addButton.clicked.connect(self.add_medicine)
        medicines = C.MedicineController.retrieve_all_medicines()
        for medicine in medicines:
            self.medMenu.addItem(medicine.name)

    def go_back(self):
        self.load_page(DoctorViewPatient())

    def edit_prescription(self):
        row = self.table.currentRow()
        C.Session.set_context('medicine_quantity', C.MedicineQuantityController.retrieve_by_id(self.table.item(row, 0).text()))
        self.load_page(DoctorEditMedicine(DoctorViewPrescription()))

    def add_medicine(self):
        try:
            selected_medicine = str(self.medMenu.currentText())
            selected_quantity = int(self.quantityLine.text())
            C.MedicineQuantityController.add_to_prescription(
                selected_quantity,
                selected_medicine,
                C.Session.get_context('prescription').object_id,
            )
            self.quantityErrorLabel.setText('')
            self.refresh_table()
        except ValueError as err:
            self.quantityErrorLabel.setText(str(err))


class PharmacistViewPrescription(ViewPrescription):
    def __init__(self):
        super(PharmacistViewPrescription, self).__init__('pharmacistViewPrescription.ui')
        widget.setFixedSize(720, 600)
        self.table.setColumnHidden(0, True)
        self.saveButton.clicked.connect(self.save_prescription)

    def go_back(self):
        self.load_page(PharmacistHome())

    def save_prescription(self):
        if prescription := C.Session.get_context('prescription'):
            prescription.collected = self.statusMenu.currentIndex()
            prescription.pharmacist_id = C.Session.get_user().object_id
            C.PrescriptionController.save_prescription(
                prescription.object_id,
                prescription.date_created,
                prescription.doctor_id,
                prescription.patient_id,
                prescription.pharmacist_id,
                prescription.collected,
            )
        self.go_back()


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
        self.table.setRowCount(0)
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

    @staticmethod
    def show_message(title, text):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(str(text))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


class AdminViewUser(ViewUser):
    def __init__(self):
        super(AdminViewUser, self).__init__('adminEditUser.ui')
        widget.setFixedSize(660, 690)
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
        password1 = self.password1Line.text()
        password2 = self.password2Line.text()
        if not (user_id and role and name and email and address and phone_number):
            self.errorLabel.setText('Please fill all fields. (Password change is optional)')
            return
        try:
            if not password1 and not password2:
                self.user_controller.save_user(user_id, email, name, phone_number, address, role)
                self.show_message('Success', 'User saved')
                self.go_back()
            else:
                if password1 != password2:
                    self.errorLabel.setText('Passwords provided do not match')
                else:
                    self.user_controller.save_user(user_id, email, name, phone_number, address, role, password1)
                    self.show_message('Success', 'User saved')
                    self.go_back()
        except ValueError as err:
            print(err)
            self.errorLabel.setText(str(err))
        except IntegrityError as err:
            print(err)         # ERROR MESSAGE SHOW ON SCREEN
            # self.show_message('Error', str(err))
            self.errorLabel.setText(str(err))

    def display_details(self):
        context_user = C.Session.get_context('user')
        index = self.userMenu.findText(context_user.role)
        if index >= 0:
            self.userMenu.setCurrentIndex(index)
        self.idLine.setText(str(context_user.object_id))
        self.nameLine.setText(context_user.name)
        self.emailLine.setText(context_user.email)
        self.addressLine.setText(context_user.address)
        self.telLine.setText(context_user.phone_number)


class DoctorViewPatient(ViewUser):
    def __init__(self, column_sizes=None):
        super(DoctorViewPatient, self).__init__('doctorViewPatient.ui')
        widget.setFixedSize(670, 590)
        # self.table.verticalHeader().setVisible(False)   # remove most left column
        if column_sizes is None:
            column_sizes = [50, 100, 150, 150, 100]
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
        widget.setFixedSize(660, 690)
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
            self.show_message('Success', 'User created')
            self.go_back()
        except ValueError as err:
            print(err)
            self.errorLabel.setText(str(err))
        except IntegrityError as err:
            print(err)
            self.errorLabel.setText(str(err))

    @staticmethod
    def show_message(title, text):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


class DoctorAddPrescription(QDialog):
    user_controller = C.UserController
    prescription_controller = C.PrescriptionController
    medicine_controller = C.MedicineController
    medicine_quantity_controller = C.MedicineQuantityController

    def __init__(self, column_sizes=None):
        super(DoctorAddPrescription, self).__init__()
        if column_sizes is None:
            column_sizes = [0, 100, 500]
        loadUi('doctorAddPrescription.ui', self)
        widget.setFixedSize(720, 615)
        self.backButton.clicked.connect(self.go_back)
        self.prescribeButton.clicked.connect(self.prescribe)
        self.addButton.clicked.connect(self.add_medicine)
        self.patientNameLine.setText(str(C.Session.get_context('user').name))
        self.table.cellClicked.connect(self.edit_medicine)
        self.table.setColumnHidden(0, True)
        for i, _ in enumerate(column_sizes):
            self.table.setColumnWidth(i, column_sizes[i])
        medicines = self.medicine_controller.retrieve_all_medicines()
        for medicine in medicines:
            self.medMenu.addItem(medicine.name)
        self.get_and_display_records()

    def get_and_display_records(self):
        self.table.setRowCount(0)
        cart = C.CartController.retrieve_cart_by_patient(C.Session.get_context('user').object_id)
        if medicine_quantities := C.MedicineQuantityController.retrieve_cart_medicines(cart.object_id):
            self.prescribeButton.setEnabled(True)
            self.table.setRowCount(len(medicine_quantities))
            for count, item in enumerate(medicine_quantities):
                medicine_name = C.MedicineController.retrieve_by_id(item.medicine_id).name
                self.table.setItem(count, 0, QTableWidgetItem(str(item.object_id)))
                self.table.setItem(count, 1, QTableWidgetItem(str(item.quantity)))
                self.table.setItem(count, 2, QTableWidgetItem(str(medicine_name)))
        else:
            self.prescribeButton.setEnabled(False)

    def go_back(self):
        widget.addWidget(DoctorViewPatient())
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def prescribe(self):
        user = C.Session.get_context('user')
        cart = C.CartController.retrieve_cart_by_patient(user.object_id)
        prescription_id = C.CartController.prescribe_medicines(cart.object_id)
        if medicine_quantities := C.MedicineQuantityController.retrieve_prescription_medicines(prescription_id):
            med_dict = {}
            for medicine_quantity in medicine_quantities:
                medicine_name = C.MedicineController.retrieve_by_id(medicine_quantity.medicine_id).name
                med_dict[medicine_name] = medicine_quantity.quantity
            qr_image = C.QRController.generate(prescription_id)
            send_email = self.sendEmailCheckbox.isChecked()
            email = C.SendEmailController(user.email, prescription_id, qr_image, user.name, med_dict, send_email)
            email.send_email()
            self.go_back()

    def add_medicine(self):
        if not self.quantityLine.text():
            return
        try:
            selected_medicine = str(self.medMenu.currentText())
            selected_quantity = int(self.quantityLine.text())
            self.medicine_quantity_controller.add_to_cart(selected_quantity, selected_medicine, C.Session.get_context('user').object_id)
            self.quantityErrorLabel.setText('')
            self.refresh_table()
        except ValueError as err:
            self.quantityErrorLabel.setText(str(err))

    def refresh_table(self):
        self.table.setRowCount(0)
        self.get_and_display_records()

    def edit_medicine(self):
        row = self.table.currentRow()
        medicine_quantity = C.MedicineQuantityController.retrieve_by_id(self.table.item(row, 0).text())
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
        widget.setFixedSize(720, 700)
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
        if not self.quantityLine.text():
            return
        medicine_quantity = C.Session.get_context('medicine_quantity')
        medicine_id = C.MedicineController.retrieve_by_name(self.medMenu.currentText()).object_id
        medicine_quantity.medicine_id = medicine_id
        medicine_quantity.quantity = int(self.quantityLine.text())
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
        self.load_page(self.back_page)

    @staticmethod
    def load_page(page):
        widget.addWidget(page)
        page.refresh_table()
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AdminAddRole(QDialog):
    def __init__(self):
        super(AdminAddRole, self).__init__()
        loadUi('adminAddRole.ui', self)
        widget.setFixedSize(660, 690)
        roles = C.UserTypeController.retrieve_all_roles()
        for role in roles:
            self.currentRolesMenu.addItem(role.role)
        self.addButton.clicked.connect(self.add_role)
        self.backButton.clicked.connect(self.go_back)

    def add_role(self):
        new_role = self.newRoleLine.text()
        print(f'{new_role = }')
        try:
            C.UserTypeController.add_role(new_role)
            self.show_message('Success', f'New role \'{new_role}\' added')
            self.go_back()
        except ValueError as err:
            print(err)
            self.errorLabel.setText(str(err))
        except IntegrityError as err:
            print(err)
            self.errorLabel.setText(str(err))

    def go_back(self):
        self.load_page(AdminHome())

    @staticmethod
    def load_page(page):
        widget.addWidget(page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def show_message(title, text):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


class Register(QDialog):
    def __init__(self):
        super(Register, self).__init__()
        loadUi("register.ui", self)
        self.registerButton.clicked.connect(self.register)
        self.backButton.clicked.connect(self.go_back)

    def register(self):
        name = self.nameLine.text()
        email = self.emailLine.text()
        address = self.addressLine.text()
        phone_number = self.telLine.text()
        password1 = self.password1Line.text()
        password2 = self.password2Line.text()
        role = 'Patient'
        if password1 != password2:
            self.errorLabel.setText('Passwords do not match')
            return
        try:
            C.UserController.create_user(email, name, phone_number, address, role, password1)
            self.go_back()
        except ValueError as err:
            print(err)
            self.errorLabel.setText(str(err))
        except IntegrityError as err:
            print(err)
            self.errorLabel.setText(str(err))

    def go_back(self):
        widget.addWidget(LoginView())
        widget.setCurrentIndex(widget.currentIndex() + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = LoginView()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main_window)
    widget.setFixedWidth(600)
    widget.setFixedHeight(530)
    widget.show()
    app.exec()
