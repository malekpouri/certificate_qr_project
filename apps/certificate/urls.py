from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, CertificateViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'certificates', CertificateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
