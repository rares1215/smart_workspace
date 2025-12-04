from django.urls import path
from .views import RegisterFormViewSet

urlpatterns = [
    path('register/', RegisterFormViewSet.as_view(), name='register_user')
]