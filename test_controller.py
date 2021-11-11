import unittest
from unittest import TestCase

from controller import (
    UserTypeController,
    UserController,
    MedicineController,
    CartController,
    PrescriptionController,
    MedicineQuantityController,
)
from entity import (
    UserType,
    User,
    Medicine,
    Cart,
    Prescription,
    MedicineQuantity
)


class TestUserTypeController(unittest.TestCase):
    def test_retrieve_all_roles(self):
        self.assertIsNotNone(UserTypeController.retrieve_all_roles())

    def test_retrieve_role(self):
        admin_user_type = UserTypeController.retrieve_role('Admin')
        doctor_user_type = UserTypeController.retrieve_role('Doctor')
        pharmacist_user_type = UserTypeController.retrieve_role('Pharmacist')
        patient_user_type = UserTypeController.retrieve_role('Patient')
        none_user_type = UserTypeController.retrieve_role('')
        self.assertTrue(admin_user_type, UserType)
        self.assertTrue(doctor_user_type, UserType)
        self.assertTrue(pharmacist_user_type, UserType)
        self.assertTrue(patient_user_type, UserType)
        self.assertFalse(none_user_type)

    def test_add_role(self):
        pass


class TestUserController(unittest.TestCase):
    def test_retrieve_all_users(self):
        self.assertIsNotNone(UserController.retrieve_all_users())

    def test_retrieve_user(self):
        self.assertIsInstance(UserController.retrieve_user(1), User)
        self.assertIsNone(UserController.retrieve_user(-1))

    def test_retrieve_users_by_role(self):
        admin_users = UserController.retrieve_users_by_role('Admin')
        doctor_users = UserController.retrieve_users_by_role('Doctor')
        pharmacist_users = UserController.retrieve_users_by_role('Pharmacist')
        patient_users = UserController.retrieve_users_by_role('Patient')
        none_users = UserController.retrieve_users_by_role('')
        self.assertTrue(admin_users)
        self.assertTrue(doctor_users)
        self.assertTrue(pharmacist_users)
        self.assertTrue(patient_users)
        self.assertFalse(none_users)

    def test_login(self):
        self.assertFalse(UserController.login('', 'password'))
        self.assertFalse(UserController.login('email', ''))
        self.assertIsInstance(UserController.login('admin@csit314.com', 'goaldiggers'), User)

    def test_check_email_match(self):
        self.assertTrue(UserController.check_email_match('admin@csit314.com'))
        self.assertFalse(UserController.check_email_match('johncena@wwe.com'))

    def test_phone_number_check(self):
        self.assertTrue(UserController.check_phone_number_match('93380000'))
        self.assertFalse(UserController.check_phone_number_match('00000000'))

    def test_encrypt_password(self):
        self.assertEqual(UserController.encrypt_password('a'),
                         'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb')

    def test_search_by_role(self):
        self.assertTrue(UserController.search_by_role('Admin'))
        self.assertTrue(UserController.search_by_role('Doctor'))
        self.assertTrue(UserController.search_by_role('Pharmacist'))
        self.assertTrue(UserController.search_by_role('Patient'))
        self.assertEqual(UserController.search_by_role(''), [])

    def test_validate_email(self):
        self.assertTrue(UserController.validate_email('example@email.com'))
        self.assertFalse(UserController.validate_email('example@email'))
        self.assertFalse(UserController.validate_email('@email.com'))
        self.assertFalse(UserController.validate_email('email'))
        self.assertTrue(UserController.validate_email('example@email.edu.au'))

    def test_validate_phone_number(self):
        self.assertTrue(UserController.validate_phone_number('86969469'))
        self.assertTrue(UserController.validate_phone_number('90000420'))
        self.assertFalse(UserController.validate_phone_number('69696969'))
        self.assertFalse(UserController.validate_phone_number('12345678'))
        self.assertTrue(UserController.validate_phone_number('90000000'))
        self.assertFalse(UserController.validate_phone_number('90000000000'))
        self.assertFalse(UserController.validate_phone_number('9000000'))


class TestPrescriptionController(TestCase):
    def test_retrieve_all_prescriptions(self):
        self.assertIsNotNone(PrescriptionController.retrieve_all_prescriptions())

    def test_retrieve_prescription(self):
        self.assertIsInstance(PrescriptionController.retrieve_prescription(1), Prescription)
        self.assertIsNone(PrescriptionController.retrieve_prescription(-1))

    def test_retrieve_patient_prescriptions(self):
        self.assertTrue(PrescriptionController.retrieve_patient_prescriptions(4))
        self.assertFalse(PrescriptionController.retrieve_patient_prescriptions(-1))


class TestMedicineController(TestCase):
    def test_retrieve_by_id(self):
        self.assertIsInstance(MedicineController.retrieve_by_id(1), Medicine)

    def test_retrieve_by_name(self):
        self.assertIsInstance(MedicineController.retrieve_by_name('ibuprophen'), Medicine)
        self.assertIsNone(MedicineController.retrieve_by_name(''))
        self.assertIsNone(MedicineController.retrieve_by_name('None'))

    def test_retrieve_all_medicines(self):
        self.assertIsNotNone(MedicineController.retrieve_all_medicines())


class TestMedicineQuantityController(TestCase):
    def test_retrieve_by_id(self):
        self.assertIsInstance(MedicineQuantityController.retrieve_by_id(1), MedicineQuantity)
        self.assertIsNone(MedicineQuantityController.retrieve_by_id(-1))

    def test_retrieve_prescription_medicines(self):
        self.assertTrue(MedicineQuantityController.retrieve_prescription_medicines(100))
        self.assertFalse(MedicineQuantityController.retrieve_prescription_medicines(-1))

    def test_retrieve_cart_medicines(self):
        self.assertTrue(MedicineQuantityController.retrieve_cart_medicines(18))
        self.assertFalse(MedicineQuantityController.retrieve_cart_medicines(-1))


class TestCartController(TestCase):
    def test_retrieve_cart_by_id(self):
        self.assertIsInstance(CartController.retrieve_cart_by_id(1), Cart)
        self.assertIsNone(CartController.retrieve_cart_by_id(-1))

    def test_retrieve_cart_by_patient(self):
        self.assertIsInstance(CartController.retrieve_cart_by_patient(4), Cart)
        # self.assertIsNone(CartController.retrieve_cart_by_patient(-1))
        with self.assertRaises(ValueError):
            CartController.retrieve_cart_by_patient(-1)


if __name__ == '__main__':
    unittest.main()
