from django.urls import path
from .views import RegisterFormViewSet,FileUploadView

urlpatterns = [
    path('register/', RegisterFormViewSet.as_view(), name='register_user'),
    path('upload/', FileUploadView.as_view(), name='upload_file'),
]