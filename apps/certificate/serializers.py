from rest_framework import serializers
from .models import Student, Certificate


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'first_name', 'last_name',
            'full_name', 'email', 'date_of_birth',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CertificateSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.UUIDField(write_only=True)
    created_by_email = serializers.EmailField(
        source='created_by.email', read_only=True)

    class Meta:
        model = Certificate
        fields = [
            'id', 'student', 'student_id', 'course_name',
            'issue_date', 'expiry_date', 'unique_code',
            'status', 'created_by_email', 'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'unique_code', 'created_by_email',
            'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        student_id = validated_data.pop('student_id')
        student = Student.objects.get(id=student_id)
        validated_data['student'] = student
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class CertificateValidationSerializer(serializers.Serializer):
    """Serializer for certificate validation endpoint."""
    unique_code = serializers.CharField()
    is_valid = serializers.BooleanField(read_only=True)
    certificate = CertificateSerializer(read_only=True)
    message = serializers.CharField(read_only=True)
