from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Student, Certificate, Course
from ..serializers import StudentSerializer, CertificateSerializer, CertificateValidationSerializer
from datetime import date, timedelta
import uuid

User = get_user_model()


class StudentSerializerTest(TestCase):
    def setUp(self):
        self.student_data = {
            'student_id': 'STU001',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'date_of_birth': date(1990, 1, 1)
        }
        self.student = Student.objects.create(**self.student_data)
        self.serializer = StudentSerializer(instance=self.student)

    def test_contains_expected_fields(self):
        """Test that serializer contains all expected fields"""
        data = self.serializer.data
        expected_fields = {
            'id', 'student_id', 'first_name', 'last_name',
            'full_name', 'email', 'date_of_birth',
            'created_at', 'updated_at'
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_full_name_field(self):
        """Test that full_name is correctly calculated"""
        data = self.serializer.data
        self.assertEqual(data['full_name'], 'John Doe')

    def test_create_student(self):
        """Test creating a new student through serializer"""
        new_student_data = {
            'student_id': 'STU002',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'date_of_birth': date(1992, 2, 2)
        }
        serializer = StudentSerializer(data=new_student_data)
        self.assertTrue(serializer.is_valid())
        student = serializer.save()
        self.assertEqual(student.student_id, 'STU002')
        self.assertEqual(student.full_name, 'Jane Smith')


class CertificateSerializerTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create test student
        self.student = Student.objects.create(
            student_id='STU001',
            first_name='John',
            last_name='Doe'
        )

        # Create test course
        self.course = Course.objects.create(
            name='Python Programming',
            description='A Python course',
            duration=10
        )

        # Create test certificate
        self.certificate_data = {
            'student': self.student,
            'course': self.course,
            'issue_date': date.today(),
            'expiry_date': date.today() + timedelta(days=365),
            'status': 'active',
            'created_by': self.user
        }
        self.certificate = Certificate.objects.create(**self.certificate_data)
        self.serializer = CertificateSerializer(instance=self.certificate)

    def test_contains_expected_fields(self):
        """Test that serializer contains all expected fields"""
        data = self.serializer.data
        expected_fields = {
            'id', 'student', 'course',
            'issue_date', 'expiry_date', 'unique_code',
            'status', 'created_by_email', 'created_at',
            'updated_at', 'signature'
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_create_certificate(self):
        """Test creating a new certificate through serializer"""
        new_certificate_data = {
            'student_id': str(self.student.id),
            'course_id': str(self.course.id),
            'issue_date': date.today(),
            'expiry_date': date.today() + timedelta(days=365),
            'status': 'active'
        }
        serializer = CertificateSerializer(
            data=new_certificate_data,
            context={'request': type('obj', (object,), {'user': self.user})}
        )
        self.assertTrue(serializer.is_valid())
        certificate = serializer.save()
        self.assertEqual(certificate.course, self.course)
        self.assertEqual(certificate.student, self.student)
        self.assertEqual(certificate.created_by, self.user)
        self.assertIsNotNone(certificate.unique_code)
        self.assertIsNotNone(certificate.signature)

    def test_read_only_fields(self):
        """Test that read-only fields are not required for creation"""
        new_certificate_data = {
            'student_id': str(self.student.id),
            'course_id': str(self.course.id),
            'issue_date': date.today(),
            'status': 'active'
        }
        serializer = CertificateSerializer(
            data=new_certificate_data,
            context={'request': type('obj', (object,), {'user': self.user})}
        )
        self.assertTrue(serializer.is_valid())


class CertificateValidationSerializerTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create test student
        self.student = Student.objects.create(
            student_id='STU001',
            first_name='John',
            last_name='Doe'
        )

        # Create test course
        self.course = Course.objects.create(
            name='Python Programming',
            description='A Python course',
            duration=10
        )

        # Create test certificate
        self.certificate = Certificate.objects.create(
            student=self.student,
            course=self.course,
            issue_date=date.today(),
            created_by=self.user
        )

    def test_validation_serializer(self):
        """Test certificate validation serializer"""
        data = {
            'unique_code': self.certificate.unique_code
        }
        serializer = CertificateValidationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
