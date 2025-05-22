from django.contrib import admin
from .models import Student, Certificate, Course


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name',
                    'email', 'date_of_birth', 'created_at')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('unique_code', 'student', 'course',
                    'issue_date', 'expiry_date', 'status', 'created_by')
    search_fields = ('unique_code', 'student__first_name',
                     'student__last_name', 'course__name')
    list_filter = ('status', 'issue_date', 'expiry_date')
    ordering = ('-created_at',)
    raw_id_fields = ('student', 'course', 'created_by')
    exclude = ('unique_code',)


admin.site.register(Course)
