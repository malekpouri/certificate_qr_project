from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import Student, Certificate, Course
import uuid
from datetime import date, timedelta
from django.core.exceptions import ValidationError

User = get_user_model()


class StudentModelTest(TestCase):
    def setUp(self):
        self.student_data = {
            'student_id': 'STU001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'date_of_birth': date(1990, 1, 1)
        }
        self.student = Student.objects.create(**self.student_data)

    def test_student_creation(self):
        """Test student creation with all fields"""
        self.assertEqual(self.student.student_id, 'STU001')
        self.assertEqual(self.student.first_name, 'John')
        self.assertEqual(self.student.last_name, 'Doe')
        self.assertEqual(self.student.email, 'john.doe@example.com')
        self.assertEqual(self.student.date_of_birth, date(1990, 1, 1))
        self.assertIsNotNone(self.student.id)
        self.assertIsInstance(self.student.id, uuid.UUID)

    def test_student_full_name(self):
        """Test the full_name property"""
        self.assertEqual(self.student.full_name, 'John Doe')

    def test_student_string_representation(self):
        """Test the string representation of the student"""
        expected_string = 'John Doe (STU001)'
        self.assertEqual(str(self.student), expected_string)

    def test_student_unique_constraint(self):
        """Test that student_id must be unique"""
        with self.assertRaises(Exception):
            Student.objects.create(
                student_id='STU001',  # Same as existing student
                first_name='Jane',
                last_name='Doe'
            )


class CertificateModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create a test student
        self.student = Student.objects.create(
            student_id='STU001',
            first_name='John',
            last_name='Doe'
        )

        # Create a test course
        self.course = Course.objects.create(
            name='Python Programming',
            description='A Python course',
            duration=10
        )

        # Create a test certificate
        self.certificate_data = {
            'student': self.student,
            'course': self.course,
            'issue_date': date.today(),
            'expiry_date': date.today() + timedelta(days=365),
            'status': 'active',
            'created_by': self.user
        }
        self.certificate = Certificate.objects.create(**self.certificate_data)

    def test_certificate_creation(self):
        """Test certificate creation with all fields"""
        self.assertEqual(self.certificate.student, self.student)
        self.assertEqual(self.certificate.course, self.course)
        self.assertEqual(self.certificate.status, 'active')
        self.assertEqual(self.certificate.created_by, self.user)
        self.assertIsNotNone(self.certificate.id)
        self.assertIsInstance(self.certificate.id, uuid.UUID)
        self.assertIsNotNone(self.certificate.unique_code)
        self.assertIsNotNone(self.certificate.signature)

    def test_certificate_string_representation(self):
        """Test the string representation of the certificate"""
        expected_string = f'Certificate for John Doe - {self.course.name}'
        self.assertEqual(str(self.certificate), expected_string)

    def test_certificate_signature_generation(self):
        """Test that signature is generated and unique"""
        # Create another course
        course2 = Course.objects.create(
            name='Java Programming',
            description='A Java course',
            duration=8
        )
        # Create another certificate
        cert2 = Certificate.objects.create(
            student=self.student,
            course=course2,
            issue_date=date.today(),
            created_by=self.user
        )

        # Check that signatures are different
        self.assertNotEqual(self.certificate.signature, cert2.signature)

        # Verify signatures
        self.assertTrue(self.certificate.verify_signature())
        self.assertTrue(cert2.verify_signature())

    def test_certificate_status_choices(self):
        """Test certificate status choices"""
        valid_statuses = ['active', 'expired', 'revoked']
        for status in valid_statuses:
            self.certificate.status = status
            self.certificate.save()
            self.assertEqual(self.certificate.status, status)

        # Test invalid status
        with self.assertRaises(ValidationError):
            self.certificate.status = 'invalid_status'
            self.certificate.full_clean()
            self.certificate.save()

    def test_certificate_unique_code_generation(self):
        """Test that unique_code is generated and unique"""
        # Create another course
        course2 = Course.objects.create(
            name='Java Programming',
            description='A Java course',
            duration=8
        )
        cert2 = Certificate.objects.create(
            student=self.student,
            course=course2,
            issue_date=date.today(),
            created_by=self.user
        )

        self.assertNotEqual(self.certificate.unique_code, cert2.unique_code)
        self.assertTrue(len(self.certificate.unique_code) > 0)
        self.assertTrue(len(cert2.unique_code) > 0)
