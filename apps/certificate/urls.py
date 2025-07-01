from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, CertificateViewSet, CourseViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
