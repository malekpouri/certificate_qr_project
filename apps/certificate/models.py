from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import uuid
import hashlib
import json
from datetime import datetime

User = get_user_model()


def validate_certificate_status(value):
    valid_statuses = ['active', 'expired', 'revoked']
    if value not in valid_statuses:
        raise ValidationError(
            f'Status must be one of: {", ".join(valid_statuses)}')


class Student(models.Model):
    """Model representing a student who can receive certificates."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.CharField(
        max_length=50, unique=True, help_text="Unique identifier for the student")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Certificate(models.Model):
    """Model representing a certificate issued to a student."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(
        'Course', on_delete=models.CASCADE, related_name='certificates')
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    unique_code = models.CharField(
        max_length=50, unique=True, help_text="Unique code for QR verification")
    signature = models.CharField(
        max_length=64, unique=True, null=True, blank=True,
        help_text="Digital signature for certificate verification")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        validators=[validate_certificate_status]
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_certificates'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['unique_code']),
            models.Index(fields=['signature']),
            models.Index(fields=['status']),
            models.Index(fields=['issue_date']),
        ]

    def __str__(self):
        return f"Certificate for {self.student.full_name} - {self.course.name}"

    def generate_signature(self):
        """Generate a digital signature for the certificate."""
        # Create a dictionary of certificate data
        cert_data = {
            'certificate_id': str(self.id),
            'student_id': self.student.student_id,
            'student_name': self.student.full_name,
            'course_name': self.course.name,
            'issue_date': self.issue_date.isoformat(),
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'unique_code': self.unique_code,
            'created_by': str(self.created_by.id) if self.created_by else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

        # Convert to JSON string and encode
        data_string = json.dumps(cert_data, sort_keys=True)
        data_bytes = data_string.encode('utf-8')

        # Generate SHA-256 hash
        signature = hashlib.sha256(data_bytes).hexdigest()
        return signature

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4())
        # Generate signature after saving to ensure created_at is available
        super().save(*args, **kwargs)
        if not self.signature:
            self.signature = self.generate_signature()
            # Save again to update the signature
            super().save(update_fields=['signature'])

    def verify_signature(self):
        """Verify the certificate's digital signature."""
        current_signature = self.generate_signature()
        return current_signature == self.signature


class Course(models.Model):
    """Model representing a course."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(help_text="Duration in weeks or hours")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name
