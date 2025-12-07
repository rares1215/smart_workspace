from django.contrib import admin
from .models import CustomUser,DocumentUpload

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(DocumentUpload)