from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class CustomUser(AbstractUser):
    pass



class DocumentUpload(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    doc_file = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)