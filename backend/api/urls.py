from django.urls import path
from .views import RegisterFormViewSet,DocumentViewSet,RAGChatView,ChatHistoryView,VerifyEmailView,ResendVerificationEmail
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='documents')

urlpatterns = [
    path('register/', RegisterFormViewSet.as_view(), name='register_user'),
    path('verify-email/<user_id>/', VerifyEmailView.as_view(), name='verify_email'),
    path('resend-email/<user_id>/', ResendVerificationEmail.as_view(), name='resend_email'),
    path('rag/<uuid:document_id>/', RAGChatView.as_view(), name='rag_query'),
    path("chat/<uuid:document_id>/", ChatHistoryView.as_view(), name="chat_history"),
]


urlpatterns += router.urls