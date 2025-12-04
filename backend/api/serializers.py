from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=30,write_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'username',
            'password',
            'password2',
        ]
        extra_kwargs = {'password':{'write_only':True}}

    #### checking the password length
    def validate_password(self,value):
        if len(value) < 10:
            raise serializers.ValidationError("The password is too short")
        return value

    ### checking if both passwords match
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':'Both passwords must match.'})
        return attrs
        
    
    #### checking if the email already exists
    def validate_email(self,value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Account already exists with this email')
        return value
    
    #### checking if username already exists
    def validate_username(self,value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists")
        return value
    
    ### creating user instance ##
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user