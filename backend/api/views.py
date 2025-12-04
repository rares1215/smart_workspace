from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework import generics,viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
# Create your views here.




#### Created the view for Register Page
class RegisterFormViewSet(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
