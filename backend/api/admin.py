from django.contrib import admin
from .models import CustomUser,DocumentUpload,ChatMessage,EmailVerification

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(DocumentUpload)
admin.site.register(ChatMessage)
admin.site.register(EmailVerification)
