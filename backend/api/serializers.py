from rest_framework import serializers
from .models import CustomUser,DocumentUpload,ChatMessage
from .utils.get_text_from_model import extract_text_from_model
import string


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

    #### checking if the password is secure enough
    def validate_password(self,value):
        if len(value) < 10:
            raise serializers.ValidationError("The password is too short")
        if not any(char in string.punctuation for char in value):
            raise serializers.ValidationError("Password must contain atleast one special character.")
        if not any(char in string.ascii_uppercase for char in value):
            raise serializers.ValidationError("Password must contain atleast one upper letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain atleast one number.")
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
    

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentUpload
        fields = [
            'id',
            'user',
            'title',
            'doc_file',
            'created_at',
            'text',
        ]
        read_only_fields = ['user','text','created_at']

    
    #### validating the size of the file to be lesser than 5MB
    def validate_doc_file(self,value):
        MAX_SIZE = 5*1024*1024
        if value.size > MAX_SIZE:
            raise serializers.ValidationError("The file is to big.")
        return value
    
    def validate(self,attrs):
        #### checking if the pdf is empty or corrupt ####
        curr_file = attrs['doc_file']
        curr_text = extract_text_from_model(curr_file)

        if not curr_text:
            raise serializers.ValidationError({'doc_file':'The pdf is corrupt or it can t be read'})
        
        return attrs
    
class RagQuery(serializers.Serializer):
    query = serializers.CharField(max_length=500)



# serializers.py
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "role",
            "content",
            "created_at",
        ]
        read_only_fields = ["role", "created_at"]





### Action to verify email 
class VerifyEmailSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Verification code must contain only digits.")
        return value