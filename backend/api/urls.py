from django.urls import path
from .views import RegisterFormViewSet,FileUploadView,RAGView

urlpatterns = [
    path('register/', RegisterFormViewSet.as_view(), name='register_user'),
    path('upload/', FileUploadView.as_view(), name='upload_file'),
    path('rag/<uuid:document_id>/', RAGView.as_view(), name='rag_query'),
]