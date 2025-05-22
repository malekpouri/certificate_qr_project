from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters import rest_framework as filters
from django.http import HttpResponse
from .models import Student, Certificate, Course
from .serializers import (
    StudentSerializer, CertificateSerializer,
    CertificateValidationSerializer, CourseSerializer
)
from .utils import generate_qr_code


class StudentFilter(filters.FilterSet):
    """Filter for Student model."""
    name = filters.CharFilter(method='filter_by_name')
    date_of_birth_after = filters.DateFilter(
        field_name='date_of_birth', lookup_expr='gte')
    date_of_birth_before = filters.DateFilter(
        field_name='date_of_birth', lookup_expr='lte')

    class Meta:
        model = Student
        fields = ['student_id', 'email']

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(
            first_name__icontains=value
        ) | queryset.filter(
            last_name__icontains=value
        )


class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet for Student model."""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filterset_class = StudentFilter
    search_fields = ['first_name', 'last_name', 'student_id', 'email']
    ordering_fields = ['created_at', 'first_name', 'last_name', 'student_id']
    ordering = ['-created_at']


class CertificateFilter(filters.FilterSet):
    """Filter for Certificate model."""
    student_name = filters.CharFilter(method='filter_by_student_name')
    course = filters.CharFilter(
        field_name='course__name', lookup_expr='icontains')
    issue_date = filters.DateFilter()
    expiry_date = filters.DateFilter()

    def filter_by_student_name(self, queryset, name, value):
        return queryset.filter(
            student__first_name__icontains=value
        ) | queryset.filter(
            student__last_name__icontains=value
        )

    class Meta:
        model = Certificate
        fields = ['student_name', 'course',
                  'issue_date', 'expiry_date', 'status']


class CertificateViewSet(viewsets.ModelViewSet):
    """ViewSet for Certificate model."""
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filterset_class = CertificateFilter
    search_fields = [
        'course__name', 'student__first_name',
        'student__last_name', 'student__student_id'
    ]
    ordering_fields = [
        'created_at', 'issue_date', 'expiry_date',
        'course__name', 'status'
    ]
    ordering = ['-created_at']

    @action(detail=True, methods=['get'], permission_classes=[], url_path='qr-code')
    def qr_code(self, request, pk=None):
        """Generate QR code for a certificate."""
        certificate = self.get_object()
        qr_buffer = generate_qr_code(certificate)
        response = HttpResponse(qr_buffer.getvalue(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="certificate_{certificate.id}_qrcode.png"'
        return response

    @action(detail=False, methods=['post'], permission_classes=[], url_path='validate')
    def validate(self, request):
        """Validate a certificate by its unique code."""
        unique_code = request.data.get('unique_code')
        if not unique_code:
            return Response(
                {'error': 'Unique code is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            certificate = Certificate.objects.get(unique_code=unique_code)
            is_valid = certificate.status == 'active'
            message = 'Certificate is valid' if is_valid else 'Certificate is not valid'

            serializer = CertificateValidationSerializer({
                'unique_code': unique_code,
                'is_valid': is_valid,
                'certificate': certificate,
                'message': message
            })
            return Response(serializer.data)

        except Certificate.DoesNotExist:
            return Response(
                {
                    'unique_code': unique_code,
                    'is_valid': False,
                    'message': 'Certificate not found'
                },
                status=status.HTTP_200_OK
            )


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course model."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name', 'duration']
    ordering = ['-created_at']
