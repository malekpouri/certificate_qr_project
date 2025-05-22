from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Student, Certificate, Course
from datetime import date, timedelta

User = get_user_model()


class StudentViewSetTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )

        # Create test student
        self.student = Student.objects.create(
            student_id='STU001',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth=date(1990, 1, 1)
        )

        # Setup API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # URLs
        self.list_url = reverse('student-list')
        self.detail_url = reverse('student-detail', args=[self.student.id])

    def test_list_students(self):
        """Test retrieving list of students"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_student(self):
        """Test creating a new student"""
        data = {
            'student_id': 'STU002',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'date_of_birth': '1992-02-02'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)

    def test_retrieve_student(self):
        """Test retrieving a specific student"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_id'], 'STU001')

    def test_update_student(self):
        """Test updating a student"""
        data = {'first_name': 'Johnny'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'Johnny')

    def test_delete_student(self):
        """Test deleting a student"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)


class CertificateViewSetTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
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

        # Setup API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # URLs
        self.list_url = reverse('certificate-list')
        self.detail_url = reverse(
            'certificate-detail', args=[self.certificate.id])
        self.validate_url = reverse('certificate-validate')

    def test_list_certificates(self):
        """Test retrieving list of certificates"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_certificate(self):
        """Test creating a new certificate"""
        data = {
            'student_id': str(self.student.id),
            'course_id': str(self.course.id),
            'issue_date': date.today().isoformat(),
            'expiry_date': (date.today() + timedelta(days=365)).isoformat(),
            'status': 'active'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Certificate.objects.count(), 2)
        self.assertIn('unique_code', response.data)
        self.assertIn('signature', response.data)

    def test_retrieve_certificate(self):
        """Test retrieving a specific certificate"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['course']['id'], str(self.course.id))
        self.assertEqual(response.data['course']['name'], self.course.name)

    def test_update_certificate(self):
        """Test updating a certificate"""
        # Create another course
        new_course = Course.objects.create(
            name='Advanced Python',
            description='Advanced Python course',
            duration=12
        )
        data = {'course_id': str(new_course.id)}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.certificate.refresh_from_db()
        self.assertEqual(str(self.certificate.course.id), str(new_course.id))

    def test_delete_certificate(self):
        """Test deleting a certificate"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Certificate.objects.count(), 0)

    def test_validate_certificate(self):
        """Test certificate validation endpoint"""
        data = {'unique_code': self.certificate.unique_code}
        response = self.client.post(self.validate_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_valid'])
        self.assertEqual(response.data['certificate']
                         ['id'], str(self.certificate.id))

    def test_validate_invalid_certificate(self):
        """Test certificate validation with invalid code"""
        data = {'unique_code': 'invalid-code'}
        response = self.client.post(self.validate_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_valid'])
