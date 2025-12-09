from django.urls import path
from .views import RegisterFormViewSet,DocumentViewSet,RAGView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='documents')

urlpatterns = [
    path('register/', RegisterFormViewSet.as_view(), name='register_user'),
    path('rag/<uuid:document_id>/', RAGView.as_view(), name='rag_query'),
]


urlpatterns += router.urls