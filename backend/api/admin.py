from django.contrib import admin
from .models import CustomUser,DocumentUpload,DocumentEmbedding

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(DocumentUpload)
admin.site.register(DocumentEmbedding)