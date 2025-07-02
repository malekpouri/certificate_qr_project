from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, CertificateViewSet, CourseViewSet
from . import views

app_name = 'certificate'

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('admin/change-user-password/', views.AdminChangeUserPasswordView.as_view(), name='admin_change_user_password'),
    path('admin/users/', views.UsersListView.as_view(), name='get_users_list'),
]
