from django.shortcuts import render
from .models import CustomUser,DocumentUpload
from .serializers import CustomUserSerializer,DocumentUploadSerializer
from rest_framework import generics,viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.parsers import MultiPartParser,FormParser
# Create your views here.




#### Created the view for Register Page
class RegisterFormViewSet(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]



###### Creating the Post Document View
class FileUploadView(generics.CreateAPIView):
    queryset = DocumentUpload.objects.all()
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]


    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)
