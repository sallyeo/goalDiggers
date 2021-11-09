import secret
import datetime
from sqlite3 import IntegrityError
import smtplib
from email.message import EmailMessage
import qrcode
import imghdr
import cv2
import entity as E
from hashlib import sha256


class Session:
    user = None
    context = {}

    @staticmethod
    def set_user(user):
        Session.user = user

    @staticmethod
    def get_user():
        return Session.user

    @staticmethod
    def set_context(key, value):
        Session.context[key] = value

    @staticmethod
    def get_context(key):
        return Session.context[key]


class UserTypeController:
    @staticmethod
    def retrieve_all_roles():
        return E.UserTypeEntity().retrieve_all()
    
    @staticmethod
    def retrieve_role(role):
        return E.UserTypeEntity().retrieve_by_id(role)

    @staticmethod
    def add_role(role):
        role = role.strip()
        if role == '':
            raise ValueError('Role can not be blank.')
        return E.UserTypeEntity().create('UserType', role=role)


class UserController:
    @staticmethod
    def retrieve_all_users():
        return E.UserEntity().retrieve_all()
        
    @staticmethod
    def retrieve_user(user_id):
        return E.UserEntity().retrieve_by_id(user_id)

    @staticmethod
    def retrieve_users_by_role(role):
        role_obj = UserTypeController.retrieve_role(role)
        if not role_obj:
            return
        return E.UserEntity().retrieve_all_by_role(role_obj.role)

    @staticmethod
    def login(email, raw_password):
        if email == "" or raw_password == "":
            return False
        encrypted = UserController.encrypt_password(raw_password)
        return E.UserEntity().validate_login(email, encrypted)

    @staticmethod
    def save_user(user_id, email, name, phone_number, address, role, password=None):
        user_id = int(user_id)
        if UserController.check_email_match(email, user_id):
            raise IntegrityError(f'Email must be unique.')
        if UserController.check_phone_number_match(phone_number, user_id):
            raise IntegrityError(f'Phone number must be unique')
        E.UserEntity().save(
            'User',
            user_id,
            email=email,
            name=name,
            phone_number=phone_number,
            address=address,
            role=role
        )
        if password is not None:
            encrypted = UserController.encrypt_password(password)
            E.UserEntity().save(
                'User',
                user_id,
                password=encrypted
            )

    @staticmethod
    def create_user(email, name, phone_number, address, role, password):
        if not email or not name or not phone_number or not address or not role or not password:
            raise ValueError('Please fill in all fields')
        # If email match
        if UserController.check_email_match(email):
            raise IntegrityError('Email must be unique.')
        # If phone number match
        if UserController.check_phone_number_match(phone_number):
            raise IntegrityError('Phone number must be unique')
        E.UserEntity().create('User', email=email, name=name, phone_number=phone_number, address=address, role=role, password=password)

    @staticmethod
    def check_email_match(email, user_id=None):
        email_check = E.UserEntity().retrieve_by_email(email)
        # If email_check list has elements and user_id is valid
        if email_check:
            if email_check.object_id != user_id:
                return True
        return False

    @staticmethod
    def check_phone_number_match(phone_number, user_id=None):
        phone_number_check = E.UserEntity().retrieve_by_phone_number(phone_number)
        # If phone_number_check list has elements and user_id is valid
        if phone_number_check:
            if phone_number_check.object_id != user_id:
                return True
        return False

    @staticmethod
    def encrypt_password(password):
        return sha256(password.encode('ascii')).hexdigest()

    @staticmethod
    def search_by_id_part(object_id_part):
        return E.UserEntity().get_many(E.UserEntity().search('User', id=object_id_part))
    
    @staticmethod
    def search_by_email_part(email_part):
        return E.UserEntity().get_many(E.UserEntity().search('User', email=email_part))

    @staticmethod
    def search_by_name_part(name_part):
        return E.UserEntity().get_many(E.UserEntity().search('User', name=name_part))

    @staticmethod
    def search_by_phone_number_part(phone_number_part):
        return E.UserEntity().get_many(E.UserEntity().search('User', phone_number=phone_number_part))
    
    @staticmethod
    def search_by_role(role):
        return E.UserEntity().get_many(E.UserEntity().search('User', role=role))


class PrescriptionController:
    e = E.PrescriptionEntity()

    @staticmethod
    def retrieve_all_prescriptions():
        return PrescriptionController.e.retrieve_all()

    @staticmethod
    def retrieve_prescription(object_id):
        return PrescriptionController.e.retrieve_by_id(object_id)

    @staticmethod
    def retrieve_patient_prescriptions(patient_id):
        return PrescriptionController.e.retrieve_by_patient(patient_id)

    @staticmethod
    def new_prescription():
        print(f"{datetime.date.today().strftime('%-d-%b-%Y')}, doctor_id = {Session.get_user().object_id}, patient_id = {Session.get_context('user').object_id}")
        date = datetime.date.today().strftime('%-d-%b-%Y')
        doctor_id = Session.get_user().object_id
        patient_id = Session.get_context('user').object_id
        prescription_id = PrescriptionController.e.create(
            'Prescription',
            date_created=date,
            doctor_id=doctor_id,
            patient_id=patient_id,
            pharmacist_id='NULL',
            collected=0,
        )
        return PrescriptionController.e.retrieve_by_id(prescription_id)

    @staticmethod
    def save_prescription(object_id, date_created, doctor_id, patient_id, pharmacist_id, collected):
        PrescriptionController.e.save(
            'Prescription',
            object_id,
            date_created=date_created,
            doctor_id=doctor_id,
            patient_id=patient_id,
            pharmacist_id=pharmacist_id,
            collected=collected,
        )

    @staticmethod
    def search_by_id_part(object_id_part):
        return PrescriptionController.e.get_many(PrescriptionController.e.search('Prescription', id=object_id_part))


class MedicineController:
    e = E.MedicineEntity()

    @staticmethod
    def retrieve_by_id(medicine_id):
        return MedicineController.e.retrieve_by_id(medicine_id)

    @staticmethod
    def retrieve_by_name(medicine_name):
        return MedicineController.e.retrieve_by_name(medicine_name)

    @staticmethod
    def retrieve_all_medicines():
        return MedicineController.e.retrieve_all()


class MedicineQuantityController:
    e = E.MedicineQuantityEntity()

    @staticmethod
    def retrieve_by_id(object_id):
        return MedicineQuantityController.e.retrieve_by_id(object_id)

    @staticmethod
    def retrieve_prescription_medicines(prescription_id):
        return MedicineQuantityController.e.retrieve_by_prescription(prescription_id)

    @staticmethod
    def retrieve_cart_medicines(cart_id):
        return MedicineQuantityController.e.retrieve_by_cart(cart_id)

    @staticmethod
    def add_to_cart(quantity, medicine_name, patient_id):
        try:
            quantity = int(quantity)
        except ValueError as err:
            print('Quantity must be an integer !')
        medicine_id = MedicineController.retrieve_by_name(medicine_name).object_id
        cart_id = CartController.retrieve_cart_by_patient(patient_id).object_id
        cart_medicines = MedicineQuantityController.e.retrieve_by_cart(cart_id)
        matched = False
        if cart_medicines:
            for medicine_quantity in cart_medicines:
                if medicine_quantity.medicine_id == medicine_id:
                    medicine_quantity.quantity += quantity
                    matched = True
                    MedicineQuantityController.e.save_object(medicine_quantity)
                    break
        if not matched:
            MedicineQuantityController.e.create('MedicineQuantity', cart_id=cart_id, medicine_id=medicine_id, quantity=quantity)

    @staticmethod
    def add_to_prescription(quantity, medicine_name, prescription_id):
        try:
            quantity = int(quantity)
        except ValueError as err:
            print('Quantity must be an integer !')
        medicine_id = MedicineController.retrieve_by_name(medicine_name).object_id
        if PrescriptionController.retrieve_prescription(prescription_id):
            prescription_medicines = MedicineQuantityController.e.retrieve_by_prescription(prescription_id)
            matched = False
            if prescription_medicines:
                for medicine_quantity in prescription_medicines:
                    print(f'looping prescription medicines: {medicine_quantity}, {medicine_id = }')
                    if medicine_quantity.medicine_id == medicine_id:
                        medicine_quantity.quantity += quantity
                        MedicineQuantityController.e.save_object(medicine_quantity)
                        matched = True
                        break
            if not matched:
                MedicineQuantityController.e.create(
                    'MedicineQuantity',
                    prescription_id=prescription_id,
                    medicine_id=medicine_id,
                    quantity=quantity,
                )
        else:
            raise IntegrityError(f'No Prescription row with id={prescription_id}')

    @staticmethod
    def save_medicine_quantity(object_id, prescription_id, cart_id, medicine_id, quantity):
        object_id = int(object_id)
        medicine_quantity = MedicineQuantityController.e.retrieve_by_id(object_id)
        medicine_quantity.prescription_id = prescription_id
        medicine_quantity.cart_id = cart_id
        medicine_quantity.medicine_id = medicine_id
        medicine_quantity.quantity = quantity
        MedicineQuantityController.e.save_object(medicine_quantity)

    @staticmethod
    def delete(object_id):
        MedicineQuantityController.e.delete('MedicineQuantity', id=object_id)


class CartController:
    e = E.CartEntity()
    
    @staticmethod
    def retrieve_cart_by_id(object_id):
        return CartController.e.retrieve_by_id(object_id)

    @staticmethod
    def retrieve_cart_by_patient(object_id):
        user = UserController.retrieve_user(object_id)
        if user.role != 'Patient':
            raise ValueError('User is not a patient.')
        cart = CartController.e.retrieve_by_patient(object_id)
        if not cart:
            CartController.e.create('Cart', patient_id=object_id)
            cart = CartController.e.retrieve_by_patient(object_id)
        return cart
    
    @staticmethod
    def create_patient_cart(patient_id):
        return CartController.e.create('Cart', patient_id=patient_id)

    @staticmethod
    def prescribe_medicines(cart_id):
        medicine_quantities = MedicineQuantityController.retrieve_cart_medicines(cart_id)
        if not medicine_quantities:
            return False
        prescription_id = PrescriptionController.new_prescription().object_id
        for medicine_quantity in medicine_quantities:
            medicine_quantity.prescription_id = prescription_id
            medicine_quantity.cart_id = 'NULL'
            MedicineQuantityController.save_medicine_quantity(
                medicine_quantity.object_id,
                medicine_quantity.prescription_id,
                medicine_quantity.cart_id,
                medicine_quantity.medicine_id,
                medicine_quantity.quantity,
            )
        return prescription_id


class QRController:
    @staticmethod
    def generate(string_code):
        img = qrcode.make(str(string_code))
        file_name = f'qrcodes/{string_code}.png'
        img.save(file_name)
        return file_name

    @staticmethod
    def read():
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        while True:
            _, img = cap.read()
            data, one, _ = detector.detectAndDecode(img)
            if data:
                code = data
                break
            cv2.imshow('sqcodescanner app', img)
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyAllWindows()
        return code


class SendEmailController:
    def __init__(self, recipient, image, recipient_name, medicine_quantities, send=True):
        self.recipient = recipient
        self.image = image
        self.recipient_name = recipient_name
        self.send = send
        medicine_amounts = []
        for key, value in medicine_quantities.items():
            medicine_amounts.append(f'{value} {key}')
        self.breakdown = '\n - '.join(medicine_amounts)
        print(f'{self.breakdown = }')

    def send_email(self):
        message = EmailMessage()
        message['Subject'] = 'GoalDiggers Email Test'
        message['From'] = secret.email
        message['To'] = self.recipient
        body = f'Good day {self.recipient_name},\n\n' \
               f'This is the breakdown of your prescription today:\n' \
               f'{self.breakdown}\n\n' \
               f'Please show the QR Code attached to the pharmacist for your prescription to be dispensed.\n\n' \
               f'Thank you'
        message.set_content(body)

        with open(self.image, 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name

        message.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

        if self.send:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(secret.email, secret.password)
                smtp.send_message(message)
